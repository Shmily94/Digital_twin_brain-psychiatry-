# -*- coding: utf-8 -*- 
# @Time : 2022/8/20 21:04 
# @Author : lepold
# @File : test_simulation.py


import argparse
import os

import numpy as np
import torch

from simulation.simulation import simulation

def get_args():
    parser = argparse.ArgumentParser(description="Model simulation")
    parser.add_argument("--ip", type=str, default="10.5.4.1:50051")     # 与server的通信ip
    parser.add_argument("--block_dir", type=str, default=None)          # 连接表路径
    parser.add_argument("--dtype", type=str, default='single')  
    parser.add_argument("--write_path", type=str, default=None)         
    parser.add_argument("--hp_after_da_path", type=str, default=None)
    parser.add_argument("--hp_after_task_da_path", type=str, default=None)
    parser.add_argument("--hp_index", type=str, default="10 12")
    parser.add_argument("--hp_a_index", type=str, default="10 12")
    parser.add_argument("--tau_index", type=str, default="20")
    parser.add_argument("--mean_brain", type=bool, default=False)
    parser.add_argument("--hp_bias", type=float, default=None)
    parser.add_argument("--name", type=str, default=None)
    parser.add_argument("--gui", type=str, default=None)
    parser.add_argument("--tau", type=str, default=None)
    parser.add_argument("--ou", type=str, default="4 0.4 0.15")
    parser.add_argument("--I_ext", type=float, default=None)
    parser.add_argument("--stimulus_region", type=str, default=None)
    parser.add_argument("--full_region", type=str, default=None)
    parser.add_argument("--manipulate_region", type=str, default=None)
    parser.add_argument("--hp_index_manipulate", type=str, default="12")
    parser.add_argument("--gui_manipulate", type=str, default="0.00565657")
    # parser.add_argument("--noise_rate", type=float, default=None)
    parser.add_argument("--step", type=int, default=800)
    parser.add_argument("--observation", type=int, default=100)
    args = parser.parse_args()
    return args

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

def change_tau(model, tau, tau_index):
    """
    simulation of resting brain at micro-column version.

    Parameters
    ----------
    model: simulation class
        实例化的simulation类

    tau: ndarray
        更新的gui值

    Returns
    -------

    """
    population_info = torch.stack(
        torch.meshgrid(model.population_id, torch.tensor(tau_index, dtype=torch.int64, device="cuda:0")),
        dim=-1).reshape((-1, 2))
    model.block_model.assign_property_by_subblk(population_info, tau.reshape(-1))

    return

def rest_simulation(args):
    """
    simulation of resting brain at micro-column version.

    Parameters
    ----------
    args: dict
        some needed parameter in simulation object.

    Returns
    -------

    """

    block_path = os.path.join(args.block_dir, "module", args.dtype)

    # if args.noise_rate is not None:
    #     print('change noise_rate to :{}'.format(args.noise_rate))
    #     block_read_path = block_path
    #     block_list = os.listdir(block_read_path)
    #     block_write_path = os.path.join(args.write_path,'blocks')
    #     os.makedirs(block_write_path, exist_ok=True)
    #     for i in range(len(block_list)):
    #         block = np.load(os.path.join(block_read_path,block_list[i]))
    #         block = dict(block)
    #         block['property'][:,0] = args.noise_rate
    #         np.savez(os.path.join(block_write_path,block_list[i]),
    #                  property=block['property'],output_neuron_idx=block['output_neuron_idx'],
    #                  input_block_idx=block['input_block_idx'], input_neuron_idx=block['input_neuron_idx'],
    #                  input_channel_offset=block['input_channel_offset'],weight=block['weight'])
    #         print('{} done!'.format(block_list[i]))
    #     block_path = block_write_path

    model = simulation(args.ip, block_path, dt=1., route_path=None, column=False, print_info=False, vmean_option=True,
                       sample_option=True, name=args.name, write_path=args.write_path)
    
    atlas_info_path = os.path.join(args.block_dir, "supplementary_info", "atlas_region.npz")
    atlas_region = np.load(atlas_info_path)['atlas_region']
    uni_region = np.load(atlas_info_path)['uni_region']
    is_cortex = np.load(atlas_info_path)['is_cortex']
    region_in_data = np.load(atlas_info_path)['region_in_data']
    uni_region = uni_region[region_in_data]
    is_cortex = is_cortex[region_in_data]
    population_base = np.load(os.path.join(args.block_dir, "supplementary_info", "population_base.npy"))
    model.sample(atlas_region, uni_region, is_cortex, population_base,num_neurons_per_voxel=250)
    
    is_task = False
    stimulus_population = None
    
    if args.gui is not None:
        gui = np.array([float(s) for s in args.gui.split()]).reshape(-1)
        hp_index = np.array([int(s) for s in args.hp_index.split()]).reshape(-1)
        gui_p = np.tile(gui,(model.num_populations, 1))
        gui_p = torch.from_numpy(gui_p.astype(np.float32)).cuda()
        print("gui = {}, hp_index = {}".format(gui, hp_index))
        change_gui(model,gui_p,hp_index)

    if args.hp_after_da_path is None:
        hp_path = None
        hp_index = None
    else:
        hp_path = args.hp_after_da_path
        hp_index = np.array([int(s) for s in args.hp_a_index.split()]).reshape(-1)
        if args.hp_bias is not None:
          hp_bias = args.hp_bias
          hp_total = np.load(hp_path)
          hp_total[:,:,0] = hp_total[:,:,0] + hp_bias
          hp_path = os.path.join(args.block_dir, "supplementary_info", "hp_rest_biased.npy")
          np.save(hp_path, hp_total)
        if args.mean_brain:
            mean_hp_after_da = np.load(hp_path)[50:, ].mean(axis=0)
            mean_hp_after_da = torch.from_numpy(mean_hp_after_da.astype(np.float32)).cuda()
            print('mean_hp_after_da.shape = {}'.format(mean_hp_after_da.shape))
            assert mean_hp_after_da.shape[0] == model.num_populations
            assert mean_hp_after_da.shape[1] == len(hp_index)
            change_gui(model,mean_hp_after_da,hp_index)
            hp_path = None
            hp_index = None
        
    if args.tau is not None:
        tau = np.array([float(s) for s in args.tau.split()]).reshape(-1)
        tau_index = np.array([int(s) for s in args.tau_index.split()]).reshape(-1)
        tau_p = np.tile(tau,(model.num_populations, 1))
        tau_p = torch.from_numpy(tau_p.astype(np.float32)).cuda()
        print("tau = {}, tau_index = {}".format(tau, tau_index))
        change_tau(model,tau_p,tau_index)

    if args.hp_after_task_da_path is not None:
        # prepare task parameter
        hp_index = np.array([2])
        hp_path = args.hp_after_task_da_path
        is_task = True
        stimulus_region = np.array([int(s) for s in args.stimulus_region.split()]).reshape(-1)
        voxel_id = np.array(range(len(atlas_region)))
        stimulus_population = (voxel_id[np.isin(atlas_region,stimulus_region)] * 2).astype(np.int64)
        stimulus_population = torch.from_numpy(stimulus_population).cuda()
        model.set_print_info(torch.tensor(voxel_id[np.isin(atlas_region, stimulus_region)], dtype=torch.int64, device="cuda:0"))
        if args.full_region is not None:
                full_region = np.array([int(s) for s in args.full_region.split()]).reshape(-1)
                assert np.all(np.isin(stimulus_region, full_region))
                atlas_region_in = atlas_region[np.isin(atlas_region, full_region)]
                hp_full = np.load(hp_path)
                print('hp_full.shape is {}'.format(hp_full.shape))
                hp_stimulus = hp_full[:,np.isin(atlas_region_in, stimulus_region),:]
                hp_path = os.path.join(args.block_dir, "supplementary_info", args.stimulus_region+'_hp.npy')
                np.save(hp_path,hp_stimulus)
        print('hp_path is {}'.format(hp_path))
        print('model.print_bold_id is {}'.format(model.print_bold_id))
        print('stimulus_population.shape is {}'.format(stimulus_population.shape))
        
    if args.manipulate_region is not None:
        gui_manipulate = np.array([float(s) for s in args.gui_manipulate.split()]).reshape(-1)
        hp_index_manipulate = np.array([int(s) for s in args.hp_index_manipulate.split()]).reshape(-1)   
         
        print("manipulate hp {} to {}".format(hp_index_manipulate,gui_manipulate)) 
             
        manipulate_region = np.array([int(s) for s in args.manipulate_region.split()]).reshape(-1)
        voxel_id = np.array(range(len(atlas_region)))
        manipulate_population = (voxel_id[np.isin(atlas_region,manipulate_region)] * 2).astype(np.int64)
        manipulate_population = torch.from_numpy(manipulate_population).cuda()
        
        gui_manipulate = np.tile(gui_manipulate,(len(manipulate_population), 1))
        gui_manipulate = torch.from_numpy(gui_manipulate.astype(np.float32)).cuda()
        
        for k in hp_index_manipulate:
            model.gamma_initialize(k, manipulate_population)
        
        manipulate_population_info = torch.stack(
        torch.meshgrid(manipulate_population, torch.tensor(hp_index_manipulate, dtype=torch.int64, device="cuda:0")),
        dim=-1).reshape((-1, 2))
        model.block_model.mul_property_by_subblk(manipulate_population_info, gui_manipulate.reshape(-1))
        

    # 添加外部刺激模块
    # 生成虚拟的hp序列来进行刺激实验
    if args.I_ext is not None:
        I_ext = args.I_ext
        if args.stimulus_region is not None:
            stimulus_region = np.array([int(s) for s in args.stimulus_region.split()]).reshape(-1)
            voxel_label = np.array(range(len(atlas_region)))
            population_id = torch.tensor(2 * voxel_label[np.isin(atlas_region, stimulus_region)], dtype=torch.int64, device="cuda:0")
            print('population_id is {}'.format(population_id))
            model.set_print_info(torch.tensor(voxel_label[np.isin(atlas_region, stimulus_region)], dtype=torch.int64, device="cuda:0"))
            print('model.print_bold_id is {}'.format(model.print_bold_id))
        else:
            population_id = model.population_id
        model.gamma_initialize(2, population_id)
        population_info = torch.stack(
            torch.meshgrid(population_id, torch.tensor([2], dtype=torch.int64, device="cuda:0")),
            dim=-1).reshape((-1, 2))
        i_ext = np.zeros((len(population_id),))
        print('i_ext.shape is {}'.format(i_ext.shape))
        print('I_ext is {}'.format(I_ext))
        i_ext[:] = I_ext
        i_ext = torch.from_numpy(i_ext.astype(np.float32)).cuda()
        model.block_model.mul_property_by_subblk(population_info, i_ext)

    
    step = args.step
    observation = args.observation
    print("step = {}, observation = {}".format(step, observation))
    print("hp_index = {}, hp_path = {}".format(hp_index, hp_path))

    # model.block_model.update_ou_background_stimuli(torch.tensor([10]).type(torch.float32).cuda(),
    #                                                   torch.tensor([0.66262627]).type(torch.float32).cuda(),
    #                                                   torch.tensor([0.12121212]).type(torch.float32).cuda(),)

    ou_paras = np.array([float(s) for s in args.ou.split()]).reshape(-1)
    print("ou_paras is {}".format(ou_paras))
    ou_tau = torch.ones(model.block_model.subblk_id.shape[0]) * torch.tensor(ou_paras[0], dtype=torch.float32)# time constant 
    ou_mean = torch.ones(model.block_model.subblk_id.shape[0])* torch.tensor(ou_paras[1], dtype=torch.float32)# mean of the ou
    ou_sigma = torch.ones(model.block_model.subblk_id.shape[0]) * torch.tensor(ou_paras[2], dtype=torch.float32) # std. dev. 
    model.block_model.update_ou_background_stimuli(model.block_model.subblk_id, ou_tau.cuda(), ou_mean.cuda(), ou_sigma.cuda())
    # model.block_model.update_ou_background_stimuli(torch.tensor(ou_paras[0]).type(torch.float32).cuda(),
    #                                                   torch.tensor(ou_paras[1]).type(torch.float32).cuda(),
    #                                                   torch.tensor(ou_paras[2]).type(torch.float32).cuda(),)
    model.clear_mode()
    model(step=step, observation_time=observation, hp_index=hp_index, hp_path=hp_path, is_task=is_task, stimulus_population=stimulus_population)


if __name__ == "__main__":
    args = get_args()
    rest_simulation(args)
