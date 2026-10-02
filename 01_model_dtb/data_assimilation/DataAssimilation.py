# -*- coding: utf-8 -*-
# @Time : 2022/8/10 11:20
# @Author : wy36
# @File : DataAssimilation.py


import os
import time
import torch
import numpy as np
from simulation.simulation import simulation
import matplotlib.pyplot as mp
from default_params import bold_params
from models.bold_model_pytorch import BOLD

mp.switch_backend('Agg')


def get_bold_signal(bold_path, b_min=None, b_max=None, lag=0):
    bold_y = np.load(bold_path)[lag:]
    if b_max is not None:
        bold_y = b_min + (b_max - b_min) * (bold_y - bold_y.min()) / (bold_y.max() - bold_y.min())
    return numpy2torch(bold_y)


def torch2numpy(u, is_cuda=True):
    assert isinstance(u, torch.Tensor)
    if is_cuda:
        return u.cpu().numpy()
    else:
        return u.numpy()


def numpy2torch(u, is_cuda=True):
    assert isinstance(u, np.ndarray)
    if is_cuda:
        return torch.from_numpy(u).cuda()
    else:
        return torch.from_numpy(u)


def diffusion_enkf(w_hat, bold_sigma, bold_t, solo_rate, debug=False):
    ensembles, brain_num, state_num = w_hat.shape
    w = w_hat.clone()  # ensemble, brain_n, hp_num+hemodynamic_state
    w_mean = torch.mean(w_hat, dim=0, keepdim=True)
    w_diff = w_hat - w_mean
    w_cx = w_diff[:, :, -1] * w_diff[:, :, -1]
    w_cxx = torch.sum(w_cx, dim=0) / (ensembles - 1) + bold_sigma
    temp = w_diff[:, :, -1] / (w_cxx.reshape([1, brain_num])) / (ensembles - 1)  # (ensemble, brain)
    # kalman = torch.mm(temp.T, w_diff.reshape([ensembles, brain_num*state_num]))  # (brain_n, brain_num*state_num)
    bold_with_noise = bold_t + bold_sigma ** 0.5 * torch.normal(0, 1, size=(ensembles, brain_num)).type_as(bold_t)
    w += solo_rate * (bold_with_noise - w_hat[:, :, -1])[:, :, None] * torch.sum(temp[:, :, None] * w_diff, dim=0,
                                                                                 keepdim=True)
    w += (1 - solo_rate) * torch.mm(torch.mm(bold_with_noise - w_hat[:, :, -1], temp.T) / brain_num,
                                    w_diff.reshape([ensembles, -1])).reshape(w_hat.shape)
    if debug:
        w_debug = w_hat[:, :10, -1][None, :, :] + (bold_with_noise - w_hat[:, :, -1]).T[:, :, None] \
                  * torch.mm(temp.T, w_diff[:, :10, -1])[:, None, :]  # brain_num, ensemble, 10
        return w, w_debug
    else:
        print(w_cxx.max(), w_cxx.min(), w[:, :, :-6].max(), w[:, :, :-6].min())
        return w


class DataAssimilation(simulation):
    """
    This is for micro-column version or voxel version.

    Specifically, for micro-column version, the overlap=10 and voxel version 1.
    It means that in DA procedure, the step units in indexing the populations between ensembles.

    """

    def __init__(self, block_path: str, ip: str, dt=1, route_path=None, column=True, **kwargs):
        """
        By giving the iP and block path, a DataAssimilation object is initialized.
        Usually in the case: 100 ensemble, i.e., 100 simulation ensemble.

        Parameters
        ----------

        block_path: str
            the dir which saves the block.npz

        ip: str
            the server listening address

        route_path : str, default is None
            the routing results.

        column: bool, default is False
            For micro-column version if column is true else for voxel

        kwargs: other positional params which are specified.

        """
        # 生成了一个block*ensemble数量的大模型
        super(DataAssimilation, self).__init__(ip, block_path, dt, route_path, column, **kwargs)
        self.device = "cuda:0"
        self._ensemble_number = kwargs.get("ensemble", 100)
        assert (self.num_neurons % self._ensemble_number == 0)
        self._hidden_state = None
        self._property_index = None
        self._index_da_voxel_pblk = None  # for bold single
        self._hp_index_updating = None  # shape=(ensemble_n*num_da_population_pblk*hp_num, 2)
        self._hp_log = None  # shape=(ensemble_n, num_da_population_pblk*hp_num)
        self._hp = None  # shape=(ensemble_n* num_da_population_pblk*hp_num)
        self._hp_low = None  # shape=(num_da_population_pblk*hp_num)
        self._hp_high = None  # shape=(num_da_population_pblk*hp_num)
        self._hp_num = None  # len(property)
        self.for_hidden_state = None
        self.from_hidden_state = None
        self.num_populations_in_one_ensemble = int(self.num_populations / self.ensemble_number)
        self.populations_id = self.block_model.subblk_id.cpu().numpy()
        print("len(populations_id)", len(self.populations_id))
        self.neurons = self.block_model.neurons_per_subblk
        self.populations_id_per_ensemble = np.split(self.populations_id, self.ensemble_number)

    @staticmethod
    def log_torch(val, lower, upper, scale=10):
        val_shape = val.shape
        assert len(lower.shape) == 1
        assert val_shape[-1] == lower.shape[-1]
        val = val.reshape(-1, lower.shape[-1])
        if (val >= upper).all() or (val <= lower).all():
            print('val <= upper).all() and (val >= lower).all()?')
        if isinstance(val, torch.Tensor):
            out = scale * (torch.log(val - lower) - torch.log(upper - val))
            return out.reshape(val_shape)
        elif isinstance(val, np.ndarray):
            out = scale * (np.log(val - lower) - np.log(upper - val))
            return out.reshape(val_shape)
        else:
            print('torch.Tensor or np.ndarray?')

    @staticmethod
    def sigmoid_torch(val, lower, upper, scale=10):
        val_shape = val.shape
        assert len(lower.shape) == 1
        assert val_shape[-1] == lower.shape[-1]
        val = val.reshape(-1, lower.shape[-1])
        if isinstance(val, torch.Tensor):
            out = lower + (upper - lower) * torch.sigmoid(val / scale)
            return out.reshape(val_shape)
        elif isinstance(val, np.ndarray):
            out = lower + (upper - lower) * 1 / (1 + np.exp(-val.astype(np.float32) / scale))
            return out.reshape(val_shape)
        else:
            print('torch.Tensor or np.ndarray?')

    @staticmethod
    def plot_bold(path_out, bold_real, bold_da, bold_index):
        steps = bold_da.shape[0]
        iteration = [i for i in range(steps)]
        assert len(bold_da.shape) == 3
        for i in bold_index:
            print("show_bold" + str(i))
            fig = mp.figure(figsize=(8, 4), dpi=500)
            ax1 = fig.add_subplot(1, 1, 1)
            ax1.plot(iteration, bold_real[:steps, i], 'r-')
            ax1.plot(iteration, np.mean(bold_da[:steps, :, i], axis=1), 'b-')
            if bold_da.shape[1] != 1:
                mp.fill_between(iteration, np.mean(bold_da[:steps, :, i], axis=1) -
                                np.std(bold_da[:steps, :, i], axis=1), np.mean(bold_da[:steps, :, i], axis=1)
                                + np.std(bold_da[:steps, :, i], axis=1), color='b', alpha=0.2)
            mp.ylim((0.0, 0.08))
            ax1.set(xlabel='observation time/800ms', ylabel='bold', title=str(i + 1))
            mp.savefig(os.path.join(path_out, "figure/bold" + str(i) + ".pdf"), bbox_inches='tight', pad_inches=0)
            mp.close(fig)

    @staticmethod
    def plot_hp(path_out, hp_real, hp, bold_index, hp_num, label='hp'):
        steps = hp.shape[0]
        iteration = [i for i in range(steps)]
        assert len(hp.shape) == 4
        for i in bold_index:
            for j in range(hp_num):
                print("show_hp", i, 'and', j)
                fig = mp.figure(figsize=(8, 4), dpi=500)
                ax1 = fig.add_subplot(1, 1, 1)
                ax1.plot(iteration, np.mean(hp[:steps, :, i, j], axis=1), 'b-')
                if hp_real is not None:
                    ax1.plot(iteration, np.tile(hp_real[j], steps), 'r-')
                if hp.shape[1] != 1:
                    mp.fill_between(iteration, np.mean(hp[:steps, :, i, j], axis=1) -
                                    np.sqrt(np.var(hp[:steps, :, i, j], axis=1)), np.mean(hp[:steps, :, i, j], axis=1)
                                    + np.sqrt(np.var(hp[:steps, :, i, j], axis=1)), color='b', alpha=0.2)
                ax1.set(xlabel='observation time/800ms', ylabel='hyper parameter')
                mp.savefig(os.path.join(path_out, 'figure/' + label + str(i) + "_" + str(j) + ".pdf"),
                           bbox_inches='tight', pad_inches=0)
                mp.close(fig)

    @staticmethod
    def show_bold(W, bold, T, path, brain_num):
        iteration = [i for i in range(T)]
        for i in range(brain_num):
            print("show_bold" + str(i))
            fig = mp.figure(figsize=(5, 3), dpi=500)
            ax1 = fig.add_subplot(1, 1, 1)
            ax1.plot(iteration, bold[:T, i], 'r-')
            ax1.plot(iteration, np.mean(W[:T, :, i, -1], axis=1), 'b-')
            mp.fill_between(iteration, np.mean(W[:T, :, i, -1], axis=1) -
                            np.std(W[:T, :, i, -1], axis=1), np.mean(W[:T, :, i, -1], axis=1)
                            + np.std(W[:T, :, i, -1], axis=1), color='b', alpha=0.2)
            mp.ylim((0.0, 0.08))
            ax1.set(xlabel='observation time/800ms', ylabel='bold', title=str(i + 1))
            mp.savefig(os.path.join(path, "bold_" + str(i) + ".png"), bbox_inches='tight', pad_inches=0)
            mp.close(fig)
        return None

    @staticmethod
    def show_hp(hp, T, path, brain_num, hp_num, hp_real=None):
        iteration = [i for i in range(T)]
        for i in range(brain_num):
            for j in range(hp_num):
                print("show_hp", i, 'and', j)
                fig = mp.figure(figsize=(5, 3), dpi=500)
                ax1 = fig.add_subplot(1, 1, 1)
                ax1.plot(iteration, np.mean(hp[:T, :, i, j], axis=1), 'b-')
                if hp_real is None:
                    pass
                else:
                    ax1.plot(iteration, np.tile(hp_real[j], T), 'r-')
                mp.fill_between(iteration, np.mean(hp[:T, :, i, j], axis=1) -
                                np.sqrt(np.var(hp[:T, :, i, j], axis=1)), np.mean(hp[:T, :, i, j], axis=1)
                                + np.sqrt(np.var(hp[:T, :, i, j], axis=1)), color='b', alpha=0.2)
                ax1.set(xlabel='observation time/800ms', ylabel='hyper parameter')
                mp.savefig(os.path.join(path, "hp" + str(i) + "_" + str(j) + ".png"), bbox_inches='tight', pad_inches=0)
                mp.close(fig)
        return None

    @property
    def ensemble_number(self):
        return self._ensemble_number

    @property
    def _num_populations_pblk(self):
        return int(self.num_populations // self._ensemble_number)

    @property
    def _num_voxel_pblk(self):
        return int(self.num_voxels // self.ensemble_number)

    @property
    def type_int(self):
        return torch.tensor([0]).type_as(self.population_id).type(torch.int64)

    @property
    def type_float(self):
        return torch.tensor([0]).type_as(self.population_id).type(torch.float32)
    
    def supplementary_info(self, supplementary_info_path):
        atlas_info_path = os.path.join(supplementary_info_path, "atlas_region.npz")
        self.neurons_per_population_base = np.load(os.path.join(supplementary_info_path, "population_base.npy"))
        self.atlas_region = np.load(atlas_info_path)['atlas_region']
        self.uni_region = np.load(atlas_info_path)['uni_region']
        self.is_cortex = np.load(atlas_info_path)['is_cortex']
        region_in_data = np.load(atlas_info_path)['region_in_data']
        self.uni_region = self.uni_region[region_in_data]
        self.is_cortex = self.is_cortex[region_in_data]
        self.num_voxel_in_one_ensemble = len(self.atlas_region)
        if self.populations_per_voxel == 10:
            self.num_cortical_voxel_in_one_ensemble = np.sum(np.isin(self.atlas_region, self.uni_region[self.is_cortex]))
            self.neurons_per_voxel_cortical = self.block_model.neurons_per_subblk.float()[
                                          :self.num_cortical_voxel_in_one_ensemble * 8].reshape((-1, 8)).sum(axis=1)

    def da_filter_parameter(self, hp_sigma, bold_sigma, solo_rate):
        self.hp_sigma = hp_sigma
        self.bold_sigma = bold_sigma
        self.solo_rate = solo_rate

    def hp_random_initialize(self, gui_low_ppopu, gui_high_ppopu, num_da_populations_pblk=None, gui_pblk=False):
        """
        Generate initial hyper parameters of each ensemble brain samples

        Complete assignment: self._hp_low, self._hp_high, self._hp, self._hp_log, self._hp_num

        Parameters
        ----------

        gui_low_ppopu: torch.tensor, shape=(num_da_populations_pblk, hp_num)
            low bound of hyper-parameters

        gui_high_ppopu: torch.tensor, shape=(num_da_populations_pblk, hp_num)
            low bound of hyper-parameters

        num_da_populations_pblk: int
            number of populations assimilated or updated for single block

        gui_pblk: bool default=False

        Returns
        -------

        self._hp: torch.tensor float32 shape=(ensemble_number*num_da_population_pblk*hp_num)

        """
        num_da_populations_pblk = self._num_populations_pblk if num_da_populations_pblk is None \
            else num_da_populations_pblk
        if gui_pblk is True:
            gui_low_ppopu = gui_low_ppopu.repeat(num_da_populations_pblk, 1)
            gui_high_ppopu = gui_high_ppopu.repeat(num_da_populations_pblk, 1)
        assert gui_low_ppopu.shape[0] == num_da_populations_pblk
        self._hp_num = gui_low_ppopu.shape[1]
        self._hp_low = gui_low_ppopu.reshape(-1).type_as(self.type_float)
        self._hp_high = gui_high_ppopu.reshape(-1).type_as(self.type_float)
        # method 1
        # self._hp_log = torch.linspace(-7, 7, self.ensemble_number).repeat_interleave(len(self._hp_low))
        # temp = torch.linspace(-1/3 + 0.34, 1/3 + 0.34, self.ensemble_number)
        temp = torch.linspace(-1/3, 1/3, self.ensemble_number)
        self._hp_log = 10*(torch.log(temp + 1) - torch.log(1 - temp)).repeat_interleave(len(self._hp_low))
        self._hp_log = self._hp_log.type_as(self.type_float).reshape(self.ensemble_number, -1, self._hp_num)
        for i in range(self._hp_num):
            idx = np.random.choice(self.ensemble_number, self.ensemble_number, replace=False)
            self._hp_log[:, :, i] = self._hp_log[idx, :, i]
        self._hp_log = self._hp_log.reshape(self.ensemble_number, -1)
        # method 2
        # self._hp_log = 14 * torch.rand((self.ensemble_number,)+ self._hp_low.shape) - 7
        self._hp = self.sigmoid_torch(self._hp_log, self._hp_low, self._hp_high).type_as(self.type_float)
        print(self._hp.shape)
        return self._hp.reshape(-1)

    def hp_index2hidden_state(self, path_cortical_or_not=None, index_da_voxel_pblk=None):
        """
        Complete assignment: self._index_da_voxel_pblk, self.for_hidden_state, self.from_hidden_state

        Parameters
        ----------
        path_cortical_or_not: str
            path of cortical_or_not

        index_da_voxel_pblk: list
            index of voxel in single block sample to assimilate

        """
        self._index_da_voxel_pblk = torch.arange(self._num_voxel_pblk) if index_da_voxel_pblk is None \
            else torch.tensor(index_da_voxel_pblk).reshape(-1)
        if path_cortical_or_not is None:
            da_cortical_or_not = np.zeros(self._num_voxel_pblk).reshape(-1)[self._index_da_voxel_pblk] == 1
        else:
            da_cortical_or_not = np.load(path_cortical_or_not).reshape(-1)[self._index_da_voxel_pblk] == 1
        num_da_voxel = da_cortical_or_not.shape[0]
        if da_cortical_or_not.sum() == da_cortical_or_not.shape:
            self.for_hidden_state = torch.arange(num_da_voxel * 8 * self._hp_num).type_as(self.type_int)
            self.from_hidden_state = torch.arange(num_da_voxel * 8 * self._hp_num).type_as(self.type_int)
        elif da_cortical_or_not.sum() == 0:
            self.for_hidden_state = torch.arange(num_da_voxel * 2 * self._hp_num).type_as(self.type_int)
            self.from_hidden_state = torch.arange(num_da_voxel * 2 * self._hp_num).type_as(self.type_int)
        else:
            self.for_hidden_state = 10 * torch.arange(num_da_voxel).reshape(-1, 1) + torch.tensor([6, 7]).repeat(4)
            self.for_hidden_state[da_cortical_or_not] += torch.tensor([-4, -4, -2, -2, 0, 0, 2, 2])
            self.for_hidden_state = self.for_hidden_state.reshape(-1).repeat_interleave(self._hp_num)
            voxel_from_hidden_state = (8 * torch.arange(num_da_voxel).reshape(-1, 1) + torch.tensor([0, 1])).reshape(-1)
            cortical_from_hidden_state = (8 * torch.arange(num_da_voxel)[da_cortical_or_not]
                                          .reshape(-1, 1) + torch.tensor([2, 3, 4, 5, 6, 7])).reshape(-1)
            self.from_hidden_state = torch.cat((voxel_from_hidden_state, cortical_from_hidden_state), dim=0)
            self.from_hidden_state, _ = self.from_hidden_state.reshape(-1, 1).sort()
            self.from_hidden_state = (self._hp_num * self.from_hidden_state + torch.arange(self._hp_num)).reshape(-1)
            self.for_hidden_state = self.for_hidden_state.type_as(self.type_int)
            self.from_hidden_state = self.from_hidden_state.type_as(self.type_int)
        # print(self.for_hidden_state.shape, self.from_hidden_state.shape, self._index_da_voxel_pblk.shape,
        #       da_cortical_or_not.shape)

    def da_property_initialize(self, property_index, alpha, gui, index_da_population=None):
        """
        Update g_ui parameters and hyper-parameters

        Complete assignment: self._property_index, self._hp_index_updating

        Parameters
        ----------

        property_index: list
            gui index in brain property

        alpha: int
            concentration of Gamma distribution which gui parameters follows

        gui: torch.tensor float32 shape=(len(voxel_index, gui_number))
            value of hyper parameters updated

        index_da_population: torch.tensor int64
            index of voxel assimilated or updated

        """
        for p in property_index:
            self.gamma_initialize(p, alpha=alpha, beta=alpha)
        self._property_index = torch.tensor(property_index).type_as(self.type_int).reshape(-1)
        # index_da_population could be optimized
        index_da_population = self.population_id if index_da_population is None else index_da_population
        self._hp_index_updating = torch.stack((torch.meshgrid(index_da_population, self._property_index)),
                                              dim=-1).reshape(-1, 2).type_as(self.type_int)
        print(self._hp_index_updating, self._hp_index_updating[:, 1], self._hp_index_updating[:, 0], gui.shape)
        self.mul_property_by_subblk(self._hp_index_updating, gui.type_as(self.type_float).reshape(-1))

    def get_hidden_state(self, steps=800, show_info=False):
        """
        The block evolve one TR time, i.e, 800 ms as default setting.

        Complete assignment: self._hidden_state

        Parameters
        ----------
        steps: int default=800
            iter number in one observation time point.

        show_info: bool, default=False
            Show frequency and BOLD signals if show_info is True

        """
        out = torch.stack(self.evolve(step=steps, vmean_option=False, sample_option=False, bold_detail=True), dim=0).T
        out = out.reshape(self.ensemble_number, self._num_voxel_pblk, 6)[:, self._index_da_voxel_pblk]
        self._hidden_state = torch.cat((self._hp_log.reshape(self.ensemble_number, -1)[:, self.for_hidden_state]
                                        .reshape(out.shape[0], out.shape[1], -1),
                                        out), dim=2)
        if show_info:
            # print(f'self._hidden_state.shape={self._hidden_state.shape}')
            print(f'(hp_log.max, mean, min)={self._hp_log.max(), self._hp_log.mean(), self._hp_log.min()}')
            print(f'(Frequency.max, mean, min)={out[:, :, 0].max(), out[:, :, 0].mean(), out[:, :, 0].min()}')
            print(f'(BOLD.max, mean, min)={out[:, :, -1].max(), out[:, :, -1].mean(), out[:, :, -1].min()}')

    def da_evolve(self, steps=800, hp_sigma=0.25):
        """
        The block evolve one TR time, i.e, 800 ms as default setting.

        Parameters
        ----------
        steps: int, default=800
            iter number in one observation time point.

        hp_sigma: int, default=1
            Step of hyper-parameters' random walk.
            Variance of noise added to hyper-parameters

        """
        self._hp_log += torch.normal(0, hp_sigma ** 0.5, size=self._hp_log.shape).type_as(self.type_float)
        self._hp = self.sigmoid_torch(self._hp_log, self._hp_low, self._hp_high)
        print(f'(hp.max, mean, min)={self._hp.max(), self._hp.mean(), self._hp.min()}')
        self.mul_property_by_subblk(self._hp_index_updating, self._hp.type_as(self.type_float).reshape(-1))
        self.get_hidden_state(steps, show_info=True)

    def da_filter(self, bold_real_t, bold_sigma=1e-8, solo_rate=0.8, debug=False, bound=None):
        """
        Correct hidden_state by diffusion ensemble Kalman filter

        Parameters
        ----------
        bold_real_t: torch.tensor, shape=(1, single_voxel_number)
            Real BOLD signal to assimilate

        bold_sigma: int, 1e-8

        solo_rate: float, default=0.5

        debug: bool, default=False
            Return hidden_state to debug if debug is true

        bound: int, default=40
            trail

        """
        if debug:
            self._hidden_state, w_debug = diffusion_enkf(self._hidden_state, bold_sigma, bold_real_t, solo_rate, debug)
            return w_debug
        else:
            self._hidden_state = diffusion_enkf(self._hidden_state, bold_sigma, bold_real_t, solo_rate)
        self._hp_log = self._hidden_state[:, :, :-6].reshape(self.ensemble_number, -1)[:, self.from_hidden_state]
        if bound is not None:
            self._hp_log = torch.clamp(self._hp_log, -bound, bound)
        self.bold.state_update(self._hidden_state[:, :, -5:-1])

    def da_rest_run(self, bold_real, write_path, step=800, observation_times=None):
        """
        Run data assimilation to simulate the BOLD signals and estimate the hyper-parameters

        Save hyper-parameters, hidden state and draw figures

        Parameters
        ----------
        bold_real: torch.tensor, shape=(t, single_voxel_number)
            Real BOLD signal to assimilate

        write_path: str
            Path where array and fig save

        observation_times: int
            iteration time of data assimilation
            Set to observation times of BOLD signals if observation_times is None

        """
        w_save = list()
        w_fix = list()
        bold_real = bold_real.type_as(self.type_float)
        assert bold_real.shape[1] == self._index_da_voxel_pblk.shape[0]
        observation_times = bold_real.shape[0] if observation_times is None else observation_times
        for t in range(observation_times):
            start_time = time.time()
            self.da_evolve(step, hp_sigma=self.hp_sigma)
            w_save.append(torch2numpy(self._hidden_state))
            self.da_filter(bold_real[t].reshape(1, -1),bold_sigma=self.bold_sigma,solo_rate=self.solo_rate)
            w_fix.append(torch2numpy(self._hidden_state))
            if t <= 9 or t % 50 == 49 or t == (observation_times - 1):
                np.save(os.path.join(write_path, "w.npy"), w_save)
                np.save(os.path.join(write_path, "w_fix.npy"), w_fix)
            print("------------run da" + str(t) + ":" + str(time.time() - start_time))
        del w_fix
        w_save = np.stack(w_save)
        bold_assimilation = w_save[:, :, :, -1]
        hp_save_log = w_save[:, :, :, :-6].reshape(observation_times, self.ensemble_number, -1)
        del w_save
        np.save(os.path.join(write_path, "bold_assimilation.npy"), bold_assimilation)
        self.plot_bold(write_path, torch2numpy(bold_real), bold_assimilation, np.arange(10))
        hp_save_log = hp_save_log[:, :, torch2numpy(self.from_hidden_state)].reshape(observation_times,
                                                                                     self.ensemble_number, -1)
        np.save(os.path.join(write_path, "hp_log.npy"), hp_save_log)
        hp_sm = self.sigmoid_torch(hp_save_log, torch2numpy(self._hp_low), torch2numpy(self._hp_high))
        hp_sm = hp_sm.reshape(observation_times, self.ensemble_number, -1, self._hp_num)
        np.save(os.path.join(write_path, "hp_sm.npy"), hp_sm.mean(1))
        self.plot_hp(write_path, None, hp_sm, np.arange(10), self._hp_num, 'hp_sm')
        hp_ms = self.sigmoid_torch(hp_save_log.mean(1), torch2numpy(self._hp_low), torch2numpy(self._hp_high))
        hp_ms = hp_ms.reshape(observation_times, -1, self._hp_num)
        np.save(os.path.join(write_path, "hp_ms.npy"), hp_ms)
        self.plot_hp(write_path, None, np.expand_dims(hp_ms, 1), np.arange(10), self._hp_num, 'hp_ms')
        self.block_model.shutdown()

    def conditional_info_helper(self, region=(42, 43), excited=True):

        region = np.array(region)
        if not excited:
            raise NotImplementedError
        # 利用模板挑选对应脑区的体素
        voxels_belong_to_region = np.isin(self.atlas_region, region).nonzero()[0]
        
        if self.populations_per_voxel == 2:
            populations_index_belong_to_region = [np.array([0]) + 2 * i for i in
                                              voxels_belong_to_region]  # only excited
        else:
            # they are all cortical voxels, so have 8 populations.
            populations_index_belong_to_region = [np.array([0, 2, 4, 6]) + 8 * i for i in
                                              voxels_belong_to_region]  # only excited
        # populations_index_belong_to_region = [np.arange(8) + 8 * i for i in voxels_belong_to_region]
        populations_index_belong_to_region = np.concatenate(populations_index_belong_to_region).astype(np.int64)

        populations_name_belong_to_region = self.populations_id_per_ensemble[0][populations_index_belong_to_region]

        # 用population_base得到神经元id
        neurons_idx_belong_to_region = []
        for idx in populations_index_belong_to_region:
            neurons_idx_belong_to_region.append(
                np.arange(self.neurons_per_population_base[idx], self.neurons_per_population_base[idx + 1]))
        neurons_idx_belong_to_region = np.concatenate(neurons_idx_belong_to_region)
        return voxels_belong_to_region.astype(np.int64), populations_name_belong_to_region.astype(
            np.int64), neurons_idx_belong_to_region.astype(np.int64)

    def task_initial_model_voxel(self, mean_hp_after_da, stimulus_hp_range, stimulus_region=(78, 79, 80, 81), para_ind=None):
        """

        Parameters
        ----------
        mean_hp_after_da : numpy.ndarray
            mean ampa after data assimilation.
        stimulus_region : list
            labels of regions that are considered as sources in this task
        para_ind : list
            default [10]

        Returns
        -------

        """
        start = time.time()

        if para_ind is None:
            para_ind = np.array([10], dtype=np.int64)
        # assert mean_hp_after_da.shape[0] == self.num_populations_in_one_ensemble

        # 将静息态平均超参导入模型
        if mean_hp_after_da is not None:
            print("mean_hp_after_da != None")
            mean_hp_after_da = np.tile(mean_hp_after_da,(self.ensemble_number, 1))
            print("mean_hp_after_da shape is {}".format(mean_hp_after_da.shape))
            mean_hp_after_da = torch.from_numpy(mean_hp_after_da.astype(np.float32)).cuda()
            for i in para_ind:
                self.gamma_initialize(i,self.population_id)
            print("population_id shape is {}".format(self.population_id.shape))
            population_info = torch.stack(
                torch.meshgrid(self.population_id, torch.tensor(para_ind, dtype=torch.int64, device="cuda:0")),
                dim=-1).reshape((-1, 2))
            print("population_info shape is {}".format(population_info.shape))
            self.block_model.mul_property_by_subblk(population_info, mean_hp_after_da.reshape(-1))
        # 得到受刺激的体素、群体、脑区编号
        # # 有4个超参，为78, 79, 80, 81这几个脑区添加外部电流，4个超参应该是对应4个兴奋性population
        # # populations_name_belong_to_region仅包含兴奋性群体,每个voxel有4个

        if self.populations_per_voxel == 2:
            self.hp_num = 1
        else:
            self.hp_num = 4
        voxel_id_belong_to_region, populations_name_belong_to_region, neurons_idx_belong_to_region = self.conditional_info_helper(
             region=stimulus_region, excited=True)
        
        self.extern_current_voxel = torch.from_numpy(voxel_id_belong_to_region).cuda()
        self.extern_populations_name = torch.from_numpy(populations_name_belong_to_region).cuda()
        # num_extern_neurons = len(neurons_idx_belong_to_region)  # number of total neurons have to be applied current
        print('self.extern_current_voxel: {} \n {} \n\n'.format(self.extern_current_voxel.shape, self.extern_current_voxel))
        print('self.extern_populations_name: {} \n {} \n\n'.format(self.extern_populations_name.shape, self.extern_populations_name))

        # 所有ensemble的受刺激population
        record_populations_name_belong_to_region = []
        for i in range(self.ensemble_number):
            if self.populations_per_voxel == 2:
                populations_name_belong_to_region = self.extern_populations_name + self.num_voxel_in_one_ensemble * 2 * i
                record_populations_name_belong_to_region.append(populations_name_belong_to_region)
            else:
          	# 为什么此处*10，而conditional_info_helper中*8
                populations_name_belong_to_region = self.extern_populations_name + self.num_voxel_in_one_ensemble * 10 * i
                record_populations_name_belong_to_region.append(populations_name_belong_to_region)
        self.total_populations_name_belong_to_region = torch.cat(record_populations_name_belong_to_region)
        print("self.total_populations_name_belong_to_region shape is", self.total_populations_name_belong_to_region.shape)

        # print("simulation of mean brain without stimualtion")
        # for i in range(10):
        #     start = time.time()
        #     out = self.evolve(800)
        #     fre = (torch.mean(out[0] / self.block_model.neurons_per_subblk.float() * 1000, dim=0)).cpu().numpy()
        #     bold = (out[-1]).cpu().numpy()
        #     print("fre shape is {}, bold shape is {}".format(fre.shape,bold.shape))
        #     print(f"{i}th observation_time, \
        #           whole brain mean fre: {np.mean(fre):.1f},  \
        #           mean bold: {np.mean(bold):.3f}, cost time is:{time.time() - start}")
        #     print("stimulation region fre shape is {}, bold shape is {}".format(fre[self.total_populations_name_belong_to_region.cpu()].shape,bold[(self.total_populations_name_belong_to_region/2).type_as(self.type_int).cpu()].shape))
        #     print(f"{i}th observation_time, \
        #           stimulation region mean fre: {np.mean(fre[self.total_populations_name_belong_to_region.cpu()]):.1f},  \
        #           mean bold: {np.mean(bold[(self.total_populations_name_belong_to_region/2).type_as(self.type_int).cpu()]):.3f}, cost time is:{time.time() - start}")

        # 要同化的超参序号 [population_id, para_id]
        self.hp_info = torch.stack(
            torch.meshgrid(self.total_populations_name_belong_to_region, torch.tensor([2]).type_as(self.type_int).reshape(-1)),
            dim=-1).reshape(-1, 2).type_as(self.type_int)

        # gamma初始化2号参数即I_extern_Input
        self.gamma_initialize(hp_index=2, population_id=self.total_populations_name_belong_to_region, alpha=5, beta=5)
        # self.gamma_initialize(hp_index=2, population_id=self.population_id, alpha=5, beta=5)
        # print("simulation of mean brain with stimualtion")
        # for i in range(10):
        #     start = time.time()
        #     out = self.evolve(800)
        #     fre = (torch.mean(out[0] / self.block_model.neurons_per_subblk.float() * 1000, dim=0)).cpu().numpy()
        #     bold = (out[-1]).cpu().numpy()
        #     print("fre shape is {}, bold shape is {}".format(fre.shape,bold.shape))
        #     print(f"{i}th observation_time, \
        #           whole brain mean fre: {np.mean(fre):.1f},  \
        #           mean bold: {np.mean(bold):.3f}, cost time is:{time.time() - start}")
        #     print("stimulation region fre shape is {}, bold shape is {}".format(fre[self.total_populations_name_belong_to_region.cpu()].shape,bold[(self.total_populations_name_belong_to_region/2).type_as(self.type_int).cpu()].shape))
        #     print(f"{i}th observation_time, \
        #           stimulation region mean fre: {np.mean(fre[self.total_populations_name_belong_to_region.cpu()]):.1f},  \
        #           mean bold: {np.mean(bold[(self.total_populations_name_belong_to_region/2).type_as(self.type_int).cpu()]):.3f}, cost time is:{time.time() - start}")
        # # for i in range(self.ensembles):
        # #     populations_name_belong_to_region = self.extern_populations_name + self.num_voxel_in_one_ensemble * 10 * i
        # #     print(f"initialize current [2] with Gamma distribution | in ensemble {i}")
        # #     self.gamma_initialize(hp_index=2, population_id=populations_name_belong_to_region)
        # #     # ensemble_neurons_idx = neurons_idx_belong_to_region + i * self.num_neurons_in_one_ensemble
        # #     # para_info = np.stack(np.meshgrid(ensemble_neurons_idx, np.array([2], dtype=np.int64), indexing="ij"),
        # #     #                      axis=-1).reshape((-1, 2))
        # #     # para_info = torch.from_numpy(para_info).cuda()
        # #
        # #     # self.block.update_property(para_info, para.sample((num_extern_neurons,)))

        self.num_external_current_voxels = voxel_id_belong_to_region.shape[0]
        # 设定外部电流的超参上下界
        self.low_bound = np.ones((self.num_external_current_voxels, self.hp_num), dtype=np.float32) * stimulus_hp_range[0] # 这里要改，先做模拟
        self.up_bound = np.ones((self.num_external_current_voxels, self.hp_num), dtype=np.float32) * stimulus_hp_range[1] # 这里要改
        print('stimulus_hp_range is {} to {}'.format(stimulus_hp_range[0],stimulus_hp_range[1]))

        self._hp = np.linspace(self.low_bound, self.up_bound, num=3 * self.ensemble_number, dtype=np.float32)[
                  self.ensemble_number: - self.ensemble_number]
        self._hp = torch.from_numpy(self._hp).cuda()  # ensembles, num_voxel, 4
        print('self.hp.shape is {}'.format(self._hp.shape))

        self.low_bound, self.up_bound = torch.from_numpy(stimulus_hp_range[0]).cuda(), torch.from_numpy(stimulus_hp_range[1]).cuda()

        self._hp_log = self.log_torch(self._hp, self.low_bound, self.up_bound)
        self.block_model.mul_property_by_subblk(self.hp_info, self._hp.reshape(-1))

        # print("simulation of mean brain with stimualtion after updating hp")
        # for i in range(10):
        #     start = time.time()
        #     out = self.evolve(800)
        #     fre = (torch.mean(out[0] / self.block_model.neurons_per_subblk.float() * 1000, dim=0)).cpu().numpy()
        #     bold = (out[-1]).cpu().numpy()
        #     print("fre shape is {}, bold shape is {}".format(fre.shape,bold.shape))
        #     print(f"{i}th observation_time, \
        #           whole brain mean fre: {np.mean(fre):.1f},  \
        #           mean bold: {np.mean(bold):.3f}, cost time is:{time.time() - start}")
        #     print("stimulation region fre shape is {}, bold shape is {}".format(fre[self.total_populations_name_belong_to_region.cpu()].shape,bold[(self.total_populations_name_belong_to_region/2).type_as(self.type_int).cpu()].shape))
        #     print(f"{i}th observation_time, \
        #           stimulation region mean fre: {np.mean(fre[self.total_populations_name_belong_to_region.cpu()]):.1f},  \
        #           mean bold: {np.mean(bold[(self.total_populations_name_belong_to_region/2).type_as(self.type_int).cpu()]):.3f}, cost time is:{time.time() - start}")

        # # for i in range(self.ensembles):
        # #     populations_name_belong_to_region = self.extern_populations_name + self.num_voxel_in_one_ensemble * 10 * i
        # #     hp_info = torch.stack(
        # #         torch.meshgrid(populations_name_belong_to_region, torch.tensor([2]).type_as(self.type_int).reshape(-1)),
        # #         dim=-1).reshape(-1, 2).type_as(self.type_int)
        # #     # hp_info = np.stack(
        # #     #     np.meshgrid(populations_name_belong_to_region.astype(np.int64), np.array([2], dtype=np.int64),
        # #     #                 indexing="ij"),
        # #     #     axis=-1).reshape(-1, 2)
        # #     # hp_info = torch.from_numpy(hp_info).cuda()
        # #     self.block.mul_property_by_subblk(hp_info, self.hp[i].reshape(-1))

        print(f"\n=================Initial DA MODEL done! cost time {time.time() - start:.2f}==========================\n")

    def task_evolve(self, steps=800):
        """
        evolve function for task state data assimilation
        only perform simulation on extern_current_voxel

        """
        print('<<<<<<<<<<<<<<< task da evolve start, is_laminar = {} >>>>>>>>>>>>>>>'.format(self.populations_per_voxel == 10))
        start = time.time()
        # [steps, ensemble_number * extern_current_voxel_number]
        act_stimulation_region_record = torch.zeros(steps, self._ensemble_number * len(self.extern_current_voxel))
        i=0

        steps = steps if steps is not None else 800
        if self.populations_per_voxel == 10:
            for return_info in self.block_model.run(steps, freq_char=True, freqs=True, vmean=False, iou=True):
                act, *others = return_info

                act_cortical = torch.empty(size=(self._ensemble_number, self.num_cortical_voxel_in_one_ensemble, 8),
                                        device=self.device)

                for idx in range(self._ensemble_number):
                    s = idx * self.num_populations_in_one_ensemble
                    e = s + self.num_cortical_voxel_in_one_ensemble * 8
                    act_cortical[idx] = act.float()[s: e].reshape((self.num_cortical_voxel_in_one_ensemble, 8))

                act_external_voxel = (act_cortical.sum(axis=-1) / self.neurons_per_voxel_cortical)[:,
                                    self.extern_current_voxel].reshape(-1)
                bold1 = self.bold.run(torch.max(act_external_voxel, torch.tensor([1e-05]).type_as(act_cortical)))

                act_stimulation_region_record[i, :] = act_external_voxel
                i = i+1
        else:
            # freq_char 应该是为了860亿模拟准备的
            for return_info in self.block_model.run(steps, freqs=True, vmean=False, iou=True):
                Freqs, *others = return_info
                act = (Freqs.reshape(-1,self.populations_per_voxel).sum(axis=1)) / self.num_neurons_per_voxel
                act_ensemble = torch.tensor(act.reshape(self._ensemble_number, -1), device=self.device)

                act_external_voxel = act_ensemble[:, self.extern_current_voxel].reshape(-1)
                bold1 = self.bold.run(torch.max(act_external_voxel, torch.tensor([1e-05]).type_as(act_ensemble)))

                act_stimulation_region_record[i, :] = act_external_voxel
                i = i+1

        # 展示受刺激区域的Bold和发放率的均值
        fre_cpu = (torch.mean(act_stimulation_region_record * 1000, dim=0)).cpu().numpy()
        bold_cpu = (bold1).cpu().numpy()
        print('stimulation region mean fre: {}, min fre: {}, max fre: {}'.format(np.mean(fre_cpu),np.min(fre_cpu),np.max(fre_cpu)))
        print('stimulation region fre 1-10: {}'.format(fre_cpu[:10]))
        print('stimulation region mean bold: {}, min bold: {}, max bold: {}'.format(np.mean(bold_cpu),np.min(bold_cpu),np.max(bold_cpu)))
        print('stimulation region bold 1-10: {}'.format(bold_cpu[:10]))

        out1 = torch.stack(
            [self.bold.s, self.bold.q, self.bold.v, self.bold.f_in, bold1])

        w = torch.cat(
            (
                self._hp_log, act_external_voxel.reshape([self.ensemble_number, -1, 1]),
                out1.T.reshape([self.ensemble_number, -1, 5])),
            dim=2)
        self._hidden_state = w
        print('self._hidden_state.shape is {}'.format(self._hidden_state.shape))
        print('<<<<<<<<<<<<<<< task da evolve done, step = {}, cost time = {} >>>>>>>>>>>>>>>'.format(steps, time.time() - start))
        return w

    def da_task_filter(self, bold_real_t, bold_sigma=1e-8, solo_rate=0.8, debug=False, bound=None):
        """
        Correct hidden_state by diffusion ensemble Kalman filter

        Parameters
        ----------
        bold_real_t: torch.tensor, shape=(1, single_voxel_number)
            Real BOLD signal to assimilate

        bold_sigma: int, 1e-8

        solo_rate: float, default=0.5

        debug: bool, default=False
            Return hidden_state to debug if debug is true

        bound: int, default=40
            trail

        """
        if debug:
            self._hidden_state, w_debug = diffusion_enkf(self._hidden_state, bold_sigma, bold_real_t, solo_rate, debug)
            return w_debug
        else:
            self._hidden_state = diffusion_enkf(self._hidden_state, bold_sigma, bold_real_t, solo_rate)
        self._hp_log = self._hidden_state[:, :, 0]
        if bound is not None:
            self._hp_log = torch.clamp(self._hp_log, -bound, bound)
        self.bold.state_update(self._hidden_state[:, :, -5:-1])


    def da_task_run_voxel(self, bold_real, write_path, step=800, observation_times=None):
        """
        Run data assimilation to simulate the BOLD signals and estimate the hyper-parameters

        Save hyper-parameters, hidden state and draw figures

        Parameters
        ----------
        bold_real: torch.tensor, shape=(t, single_voxel_number)
            Real BOLD signal to assimilate

        write_path: str
            Path where array and fig save

        observation_times: int
            iteration time of data assimilation
            Set to observation times of BOLD signals if observation_times is None

        """
        total_start = time.time()

        path = os.path.join(write_path,'show')
        os.makedirs(path, exist_ok=True)
        print("\n==================== show hp ====================")
        print("self.hp", self._hp)
        print("self.low_bound", self.low_bound)
        print("self.up_bound", self.up_bound)
        print("self.hp_log", self._hp_log)
        print("==================== show hp ====================\n")

        self.bold = BOLD(**bold_params)

        for k in range(10):
            print("k", k)
            self.task_evolve(steps=800)

        w_save = list()
        w_fix = list()

        bold_real = bold_real.type_as(self.type_float)
        bold_real = bold_real[:, self.extern_current_voxel]
        assert bold_real.shape[1] == self.extern_current_voxel.shape[0]

        observation_times = bold_real.shape[0] if observation_times is None else observation_times

        for t in range(observation_times):
            step_start = time.time()
            print("\n==================== Processing observation {}====================\n".format(t))

            bold_real_t = bold_real[t].reshape([1, self.num_external_current_voxels])
            print('bold_real_t.shape is {}'.format(bold_real_t.shape))
            # hp random walk
            print("-------------------- hp_log random walk --------------------")
            start_randomwalk = time.time()
            self._hp_log = self._hp_log.reshape(self._hp.shape)
            print('self._hp_log.shape is {}'.format(self._hp_log.shape))
            self._hp_log = self._hp_log + (self.hp_sigma ** 0.5 * torch.normal(0, 1, size=(
                    self.ensemble_number, self.num_external_current_voxels, 1), device=self.device)).type_as(self.type_float)
            # print("self.hp_log", self.hp_log.min().item(), self.hp_log.max().item())
            self._hp = self.sigmoid_torch(self._hp_log, self.low_bound, self.up_bound)
            hp_log_cpu = self._hp_log.cpu().numpy().reshape(-1)
            print('mean hp log: {}, min hp log: {}, max hp log: {}'.format(np.mean(hp_log_cpu),np.min(hp_log_cpu),np.max(hp_log_cpu)))
            print('stimulation region hp log 1-10: {}'.format(hp_log_cpu[:10]))
            print("Hp_Cortical, eg: ", self._hp[:, 0, :].data)
            self.block_model.mul_property_by_subblk(self.hp_info, self._hp.type_as(self.type_float).reshape(-1))
            print("random walk cost time: {}".format(time.time() - start_randomwalk))

            # evolve
            print("-------------------- model evolve --------------------")
            print('real bold 1-10: {}'.format(bold_real_t[0,:10]))
            start_evolve = time.time()
            self.task_evolve(steps=step)
            w_save.append(torch2numpy(self._hidden_state))
            print("evolve cost time: {}".format(time.time() - start_evolve))

            # filter
            print("-------------------- ensemble Kalman filter --------------------")
            start_filter = time.time()
            self.da_task_filter(bold_real_t, bold_sigma=self.bold_sigma, solo_rate=self.solo_rate)
            print('self._hp_log.shape after filter is {}'.format(self._hp_log.shape))
            hp_log_cpu = self._hp_log.cpu().numpy().reshape(-1)
            print('mean hp log: {}, min hp log: {}, max hp log: {}'.format(np.mean(hp_log_cpu),np.min(hp_log_cpu),np.max(hp_log_cpu)))
            print('stimulation region hp log 1-10: {}'.format(hp_log_cpu[:10]))
            w_fix.append(torch2numpy(self._hidden_state))
            print("filter cost time: {}".format(time.time() - start_filter))
            print("-------------------- step cost time: {} --------------------".format(time.time() - step_start))

            if t <= 3 or t % 50 == 49:
                np_w_save = np.array(w_save)
                self.show_bold(np_w_save, torch2numpy(bold_real, is_cuda=True), t, path, 10)
                hp_save = self.sigmoid_torch(
                    np_w_save[:, :, :, :self.hp_num].reshape((t+1) * self.ensemble_number, self.num_external_current_voxels,
                                                          self.hp_num), torch2numpy(self.low_bound),
                    torch2numpy(self.up_bound))
                hp_save = hp_save.reshape((t+1, self.ensemble_number, self.num_external_current_voxels, self.hp_num))
                np.save(os.path.join(write_path, "hp.npy"), hp_save.mean(axis=1))
                self.show_hp(hp_save.reshape(t+1, self.ensemble_number, self.num_external_current_voxels, self.hp_num),
                             t,
                             path, 10, self.hp_num)
        
        del w_fix
        w_save = np.stack(w_save)
        print("\n                 END DA               \n")
        np.save(os.path.join(write_path, "W.npy"), w_save)

        self.show_bold(w_save, torch2numpy(bold_real, is_cuda=True), observation_times, path, 10)
        hp_save = self.sigmoid_torch(
            w_save[:, :, :, :self.hp_num].reshape(observation_times * self.ensemble_number, self.num_external_current_voxels,
                                                  self.hp_num), torch2numpy(self.low_bound),
            torch2numpy(self.up_bound))
        hp_save = hp_save.reshape((observation_times, self.ensemble_number, self.num_external_current_voxels, self.hp_num))
        np.save(os.path.join(write_path, "hp.npy"), hp_save.mean(axis=1))
        self.show_hp(hp_save.reshape(observation_times, self.ensemble_number, self.num_external_current_voxels, self.hp_num), observation_times,
                     path, 10, self.hp_num)
        self.block_model.shutdown()
        print("\n\n Totally cost time:\t", time.time() - total_start)
        print("=================================================\n")

        
