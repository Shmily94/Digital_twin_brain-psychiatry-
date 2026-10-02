import os
import shutil
import argparse
import time
import tempfile
import numpy as np
import torch
from DataAssimilation import *
from simulation.simulation import simulation


def get_args():
    parser = argparse.ArgumentParser(description="PyTorch Data Assimilation")
    parser.add_argument("--task", type=str, default="rest")
    parser.add_argument("--ip", type=str, default="10.5.4.1:50051")
    parser.add_argument("--is_cuda", type=bool, default=True)
    parser.add_argument("--block_path", type=str, default=None)
    parser.add_argument("--dtype", type=str, default="single")
    parser.add_argument("--path_out", type=str, default=None)
    parser.add_argument("--bold_idx_path", type=str, default=None)
    parser.add_argument("--para_ind", type=str, default="10 12")
    parser.add_argument("--gui", type=str, default=None)
    parser.add_argument("--hp_range_rate", type=str, default="4 2")
    parser.add_argument("--bold_range", type=str, default="0.02 0.05")
    parser.add_argument("--solo_rate", type=float, default=0.5)
    parser.add_argument("--noise_rate", type=float, default=0.01)
    parser.add_argument("--gui_alpha", type=int, default=5)
    parser.add_argument("--I_alpha", type=int, default=1)
    parser.add_argument("--T", type=int, default=None)
    parser.add_argument("--hp_sigma_2", type=float, default=0.25)
    parser.add_argument("--bold_sigma", type=float, default=1e-8)
    parser.add_argument("--ensembles", type=int, default=100)
    parser.add_argument("--sample_path", type=str, default=None)
    parser.add_argument("--gui_real", type=str, default="6.1644921e-03 8.9986715e-04 2.9690875e-02 1.9053727e-03")
    parser.add_argument("--label", type=str, default=None)
    parser.add_argument("--I_ext", type=float, default=1.)
    parser.add_argument("--ou", type=str, default="4 0.4 0.15")
    parser.add_argument("--task_bold_path", type=str, default=None)
    parser.add_argument("--w_path", type=str, default=None)
    parser.add_argument("--gui_label", type=str, default=None)
    parser.add_argument("--gui_path", type=str, default=None)
    parser.add_argument("--I_path", type=str, default=None)
    parser.add_argument("--step", type=int, default=800)
    parser.add_argument("--observation", type=int, default=None)
    parser.add_argument("--stimulus_region", type=str, default="43 44")
    parser.add_argument("--hp_after_da_path", type=str, default=None)
    parser.add_argument("--task_name", type=str, default=None)
    parser.add_argument("--stimulus_hp_range", type=str, default="0.01 0.3")
    return parser.parse_args()


def regular_dict(**kwargs):
    return kwargs


def progress_bar(progress, time):
    """ Print progress bar to console output in the format
    Progress: [######### ] 90.0% in 10.22 sec

    Parameters
    ----------
    progress : float
        Value between 0 and 1.
    time : float
        Elapsed time till current progress.
    """

    print("\r| Progress: [{0:10s}] {1:.1f}% in {2:.0f} sec".format(
        '#' * int(progress * 10), progress * 100, time), end='')
    if progress >= 1:
        print("\r| Progress: [{0:10s}] {1:.1f}% in {2:.2f} sec".format(
            '#' * int(progress * 10), progress * 100, time))

    return


def ln(subject, ensembles, dtype):
    """Create a private ensemble-block directory for the current client run.

    Every invocation creates a new directory under ``multi_module/<dtype>``.
    MID and SST clients therefore never read from or write to the same set of
    symbolic links, even when they run at the same time.
    """
    single_path = os.path.join(subject, 'module', dtype)
    ensemble_root = os.path.join(subject, 'multi_module', dtype)

    if not os.path.isdir(single_path):
        raise FileNotFoundError(
            "Source block directory does not exist: {}".format(single_path)
        )

    os.makedirs(ensemble_root, exist_ok=True)

    source_blocks = []
    for filename in os.listdir(single_path):
        if not (filename.startswith('block_') and filename.endswith('.npz')):
            continue

        index_text = filename[len('block_'):-len('.npz')]
        try:
            block_index = int(index_text)
        except ValueError:
            continue

        source_blocks.append(
            (block_index, os.path.join(single_path, filename))
        )

    source_blocks.sort(key=lambda item: item[0])
    if not source_blocks:
        raise RuntimeError(
            "No block_*.npz files found in {}".format(single_path)
        )

    # mkdtemp creates the directory atomically and guarantees that this client
    # receives a path that is not shared with another MID/SST client.
    job_name = os.environ.get('SLURM_JOB_NAME', 'local')
    job_id = os.environ.get('SLURM_JOB_ID', 'nojob')
    safe_job_name = ''.join(
        char if char.isalnum() or char in '._-' else '_'
        for char in job_name
    )
    run_prefix = '{}_{}_'.format(safe_job_name, job_id)
    ensemble_path = tempfile.mkdtemp(
        prefix=run_prefix,
        dir=ensemble_root,
    )

    num_single_blocks = len(source_blocks)
    expected_total = ensembles * num_single_blocks
    computation_start = time.time()

    print("Unique ensemble block directory: {}".format(ensemble_path))
    print(
        "Source blocks: {}, ensembles: {}, expected links: {}".format(
            num_single_blocks,
            ensembles,
            expected_total,
        )
    )

    try:
        for source_order, (_, source_path) in enumerate(source_blocks):
            progress_bar(
                source_order / num_single_blocks,
                time.time() - computation_start,
            )

            absolute_source = os.path.abspath(source_path)
            for ensemble_index in range(ensembles):
                target_index = (
                    ensemble_index * num_single_blocks + source_order
                )
                target_path = os.path.join(
                    ensemble_path,
                    'block_{}.npz'.format(target_index),
                )
                os.symlink(absolute_source, target_path)

        progress_bar(1.0, time.time() - computation_start)

        actual_total = len([
            filename
            for filename in os.listdir(ensemble_path)
            if filename.startswith('block_') and filename.endswith('.npz')
        ])
        if actual_total != expected_total:
            raise RuntimeError(
                "Incomplete ensemble directory {}: expected {} links, found {}"
                .format(ensemble_path, expected_total, actual_total)
            )

        print(
            "Ensemble block directory ready: {} ({} links)".format(
                ensemble_path,
                actual_total,
            )
        )
        return ensemble_path

    except Exception:
        # A failed run must not leave a partially generated directory that may
        # later be mistaken for a valid ensemble directory.
        shutil.rmtree(ensemble_path, ignore_errors=True)
        raise

def change_gui(model, gui, hp_index):
    """
    simulation of resting brain at micro-column version.

    Parameters
    ----------
    model: simulation class
        实例化的simulation类

    gui: ndarray
        更新的gui值

    Returns
    -------

    """
    for k in hp_index:
        model.gamma_initialize(k, model.population_id)
    population_info = torch.stack(
        torch.meshgrid(model.population_id, torch.tensor(hp_index, dtype=torch.int64, device="cuda:0")),
        dim=-1).reshape((-1, 2))
    model.block_model.mul_property_by_subblk(population_info, gui.reshape(-1))

    return

def rest_voxel(args):
    # read parameters
    property_index = np.array([int(s) for s in args.para_ind.split()]).reshape(-1)
    text_para_ind = '_'.join([str(i) for i in property_index.flatten()])
    hp_range_rate = np.array([float(s) for s in args.hp_range_rate.split()]).reshape(2, -1)
    bold_range = np.array([float(s) for s in args.bold_range.split()]).reshape(2, -1)
    text_hp_range_rate = '_'.join([str(i) for i in hp_range_rate.flatten()])
    
    # make dirs
    path_out = args.path_out + args.label + '_' + text_para_ind + '_' + text_hp_range_rate + '_' + str(args.solo_rate) + '_' + str(
        args.ensembles) + '_' + str(args.hp_sigma_2) + '/assimilation/'
    os.makedirs(path_out, exist_ok=True)
    os.makedirs(path_out + 'figure/', exist_ok=True)
    
    # get real bold signal
    bold_path = os.path.join(args.block_path,"supplementary_info", "rest_state_bold.npy")
    bold_real = get_bold_signal(bold_path, b_min=bold_range[0], b_max=bold_range[1], lag=0)
    print("bold_shape = {}, bold_min = {}, bold_max = {}".format(bold_real.shape,bold_real.min(),bold_real.max()))
    
    # da_rest
    print('=============================prepare DA configuration=========================================')
    block_path = ln(args.block_path,args.ensembles, args.dtype)
    da_rest = DataAssimilation(block_path, args.ip, column=False, ensemble=args.ensembles)
    da_rest.clear_mode()
    print('da_filter_parameter is: hp_sigma_2 = {}, bold_sigma = {}, solo_rate = {}'.format(args.hp_sigma_2, args.bold_sigma, args.solo_rate))
    da_rest.da_filter_parameter(args.hp_sigma_2, args.bold_sigma, args.solo_rate)

    ou_paras = np.array([float(s) for s in args.ou.split()]).reshape(-1)
    print("ou_paras is {}".format(ou_paras))
    ou_tau = torch.ones(da_rest.block_model.subblk_id.shape[0]) * torch.tensor(ou_paras[0], dtype=torch.float32)# time constant 
    ou_mean = torch.ones(da_rest.block_model.subblk_id.shape[0])* torch.tensor(ou_paras[1], dtype=torch.float32)# mean of the ou
    ou_sigma = torch.ones(da_rest.block_model.subblk_id.shape[0]) * torch.tensor(ou_paras[2], dtype=torch.float32) # std. dev. 
    da_rest.block_model.update_ou_background_stimuli(da_rest.block_model.subblk_id, ou_tau.cuda(), ou_mean.cuda(), ou_sigma.cuda())
    # da_rest.block_model.update_ou_background_stimuli(torch.tensor(ou_paras[0]).type(torch.float32).cuda(),
    #                                                   torch.tensor(ou_paras[1]).type(torch.float32).cuda(),
    #                                                   torch.tensor(ou_paras[2]).type(torch.float32).cuda(),)

    if args.gui_label is not None:
        gui_real = np.array([float(s) for s in args.gui_real.split()]).reshape(-1, 1)
        gui_label = np.array([int(s) for s in args.gui_label.split()]).reshape(-1)
        gui_p = np.tile(gui_real,(da_rest.num_populations, 1))
        gui_p = torch.from_numpy(gui_p.astype(np.float32)).cuda()
        print("gui = {}, gui_index = {}".format(gui_real, gui_label))
        change_gui(da_rest,gui_p, gui_label)

    # gui boundary initialize
    gui_number = len(property_index)
    gui_low = gui_real[property_index - 10] / hp_range_rate[0]  # shape = gui_number
    gui_high = gui_real[property_index - 10] * hp_range_rate[1]
    gui_low = torch.tensor(gui_low, dtype=torch.float32).reshape(1, gui_number)
    gui_high = torch.tensor(gui_high, dtype=torch.float32).reshape(1, gui_number)
    print("assimilating gui {} in [{}, {}]".format(property_index, gui_low, gui_high))
    
    # da_rest initialize
    da_gui = da_rest.hp_random_initialize(gui_low, gui_high, gui_pblk=True)
    da_rest.hp_index2hidden_state()
    da_rest.da_property_initialize(property_index, args.gui_alpha, da_gui)
    for _ in range(5):
        da_rest.get_hidden_state()
    
    # da_rest run
    print('step = {}'.format(args.step))
    print('observation = {}'.format(args.observation))
    da_rest.da_rest_run(bold_real, path_out, step=args.step, observation_times=args.observation)


def rest_laminar(args):
    # make dirs
    property_index = np.array([int(s) for s in args.para_ind.split()]).reshape(-1)
    text_para_ind = '_'.join([str(i) for i in property_index.flatten()])
    hp_range_rate = np.array([float(s) for s in args.hp_range_rate.split()]).reshape(2, -1)
    text_hp_range_rate = '_'.join([str(i) for i in hp_range_rate.flatten()])
    path_out = args.path_out + args.label + text_para_ind + text_hp_range_rate + str(args.solo_rate) + str(
        args.ensembles) + '/assimilation/'
    os.makedirs(path_out, exist_ok=True)
    os.makedirs(path_out + 'figure/', exist_ok=True)
    # get real bold signal
    bold_real = get_bold_signal(args.bold_path, b_min=0.02, b_max=0.05, lag=0)
    print('=============================prepare DA configuration=========================================')
    # da_rest
    da_rest = DataAssimilation(args.block_path, args.ip, column=True, ensemble=args.ensembles)
    da_rest.clear_mode()

    # gui boundary initialize
    gui_real = np.array([[0.00659512, 0.00093751, 0.1019024, 0.00458985],
                         [0.01381911, 0.00196363, 0.18183651, 0.00727698],
                         [0.00754673, 0.00106148, 0.09852575, 0.00431849],
                         [0.0134587, 0.00189199, 0.15924831, 0.00651926],
                         [0.00643689, 0.00091055, 0.10209763, 0.00444712],
                         [0.01647443, 0.00234132, 0.21505809, 0.00796669],
                         [0.00680198, 0.00095797, 0.06918744, 0.00324963],
                         [0.01438906, 0.00202573, 0.14674303, 0.00587307],
                         [0.00618016, 0.00086915, 0.07027743, 0.00253291]], dtype=np.float64).T
    gui_number = len(property_index)
    gui_low = gui_real[property_index - 10] / hp_range_rate[0]  # shape = gui_number
    gui_high = gui_real[property_index - 10] * hp_range_rate[1]
    gui_low = torch.tensor(gui_low, dtype=torch.float32).reshape(1, gui_number)
    gui_high = torch.tensor(gui_high, dtype=torch.float32).reshape(1, gui_number)
    # da_rest initialize
    da_gui = da_rest.hp_random_initialize(gui_low, gui_high, gui_pblk=True)
    path_cortical_or_not='/public/home/ssct004t/project/zenglb/Digital_twin_brain/data_assimilation/path_cortical_or_not.npy'
    da_rest.hp_index2hidden_state(path_cortical_or_not)
    da_rest.da_property_initialize(property_index, args.gui_alpha, da_gui)
    da_rest.get_hidden_state()
    # da_rest run
    bold_real = torch.cat((bold_real, bold_real[:, :296]), dim=1)
    da_rest.da_rest_run(bold_real, path_out)


def task_voxel(args):
    # 需要的参数：block_path、静息态同化超参的hp_after_da_path和para_ind用于生成平均脑
    # 同化外部电流的脑区编号stimulus_region，那么相应需要提供脑区序号atlas_region

    
    bold_range = np.array([float(s) for s in args.bold_range.split()]).reshape(2, -1)
    stimulus_region = np.array([int(s) for s in args.stimulus_region.split()]).reshape(-1)
    # text_stimulus_region = '_'.join([str(i) for i in stimulus_region.flatten()])
    stimulus_hp_range = np.array([float(s) for s in args.stimulus_hp_range.split()]).reshape(2, -1)
    hp_after_da_path = args.hp_after_da_path

    # hp_range_rate = np.array([float(s) for s in args.hp_range_rate.split()]).reshape(2, -1)
    # text_hp_range_rate = '_'.join([str(i) for i in hp_range_rate.flatten()])
    
    # make dirs
    path_out = args.path_out + args.label + '_' + args.task + '_' + args.task_name + '_full_' + str(stimulus_hp_range[0,0]) + '_' + str(stimulus_hp_range[1,0]) + '_' + str(args.hp_sigma_2) + '_' + str(args.solo_rate) +'_' + str(
        args.ensembles) + '/assimilation/'
    os.makedirs(path_out, exist_ok=True)
    os.makedirs(path_out + 'figure/', exist_ok=True)
    
    # get real bold signal
    bold_path = os.path.join(args.block_path,"supplementary_info", args.task_name + "_task_bold.npy")
    print("bold path is : {}".format(bold_path))
    bold_real = get_bold_signal(bold_path, b_min=bold_range[0], b_max=bold_range[1], lag=0)
    print("bold_shape = {}, bold_min = {}, bold_max = {}".format(bold_real.shape,bold_real.min(),bold_real.max()))

    supplementary_info_path = os.path.join(args.block_path,"supplementary_info")
    
    # da_task init
    print('=============================prepare DA configuration=========================================')
    block_path = ln(args.block_path,args.ensembles, args.dtype)
    da_task = DataAssimilation(block_path, args.ip, column=False, ensemble=args.ensembles)
    # 导入population_base和atlas_region等补充信息
    da_task.supplementary_info(supplementary_info_path)
    # 导入 KF 的参数 hp_sigma=0.01, bold_sigma=1e-8, solo_rate = 0.5
    print("hp_sigma_2 is {}, bold_sigma is {}, solo_rate is {}".format(args.hp_sigma_2, args.bold_sigma, args.solo_rate))
    da_task.da_filter_parameter(args.hp_sigma_2, args.bold_sigma, args.solo_rate)
    ou_paras = np.array([float(s) for s in args.ou.split()]).reshape(-1)
    print("ou_paras is {}".format(ou_paras))
    ou_tau = torch.ones(da_task.block_model.subblk_id.shape[0]) * torch.tensor(ou_paras[0], dtype=torch.float32)# time constant 
    ou_mean = torch.ones(da_task.block_model.subblk_id.shape[0])* torch.tensor(ou_paras[1], dtype=torch.float32)# mean of the ou
    ou_sigma = torch.ones(da_task.block_model.subblk_id.shape[0]) * torch.tensor(ou_paras[2], dtype=torch.float32) # std. dev. 
    da_task.block_model.update_ou_background_stimuli(da_task.block_model.subblk_id, ou_tau.cuda(), ou_mean.cuda(), ou_sigma.cuda())
    da_task.clear_mode()

    # 输入静息态脑参数
    if hp_after_da_path is None:
        mean_hp_after_da = None
        if args.gui is not None:
            gui = np.array([float(s) for s in args.gui.split()]).reshape(-1)
            da_para_ind = np.array([int(s) for s in args.para_ind.split()]).reshape(-1)
            gui_p = np.tile(gui,(da_task.num_populations, 1))
            gui_p = torch.from_numpy(gui_p.astype(np.float32)).cuda()
            print("gui = {}, hp_index = {}".format(gui, da_para_ind))
            change_gui(da_task,gui_p, da_para_ind)
    else:
        mean_hp_after_da = np.load(hp_after_da_path)[50:, ].mean(axis=0)
        da_para_ind = np.array([int(s) for s in args.para_ind.split()]).reshape(-1)
        print("mean_hp_after_da.shape", mean_hp_after_da.shape)
        print("self.num_populations_in_one_ensemble", da_task.num_populations_in_one_ensemble)
        assert mean_hp_after_da.shape[0] == da_task.num_populations_in_one_ensemble
        assert mean_hp_after_da.shape[1] == len(da_para_ind)

    # 任务态初始化，da_para_ind为静息态同化的参数序号, stimulus_region为同化外部电流的脑区编号
    da_task.task_initial_model_voxel(mean_hp_after_da, stimulus_hp_range, stimulus_region=stimulus_region, para_ind=da_para_ind)
    # da_task.block_model.shutdown()
    # da_task run
    print('step = {}'.format(args.step))
    da_task.da_task_run_voxel(bold_real,  path_out, step=args.step, observation_times=args.observation)


def rest_simulation(args):
    property_index = np.array([int(s) for s in args.para_ind.split()]).reshape(-1)
    path_out = args.path_out + args.label
    os.makedirs(path_out, exist_ok=True)
    os.makedirs(path_out + '/figure/', exist_ok=True)
    # bold_real = get_bold_signal(args.bold_path, b_min=0.02, b_max=0.05, lag=0)
    da_simulation = simulation(args.ip, args.block_path, dt=1, column=False, print_info=False, write_path=path_out)
    da_simulation.clear_mode()
    # da_simulation.block_model.print_stat = True
    # da_simulation.print_info = True
    hp_after_da = np.load(args.path_out + args.gui_path)
    #hp_after_da = np.array([float(s) for s in args.gui_real.split()]).reshape(-1)
    #hp_after_da = np.tile(hp_after_da, [50, da_simulation.num_populations, 1])[:, :, property_index-10]
    observation_time, num_da_population_pblk, hp_num = hp_after_da.shape
    print(observation_time, num_da_population_pblk, hp_num)
    hp_after_da = torch.from_numpy(hp_after_da.astype(np.float32)).cuda()
    da_simulation.run(step=args.step, observation_time=observation_time-1, hp_index=property_index, hp_total=hp_after_da)
    da_simulation.block_model.shutdown()


if __name__ == "__main__":
    args = get_args()
    if args.task == 'rest':
        rest_voxel(args)
    if args.task == 'task':
        task_voxel(args)
    if args.task == 'rest simulation':
        rest_simulation(args)
