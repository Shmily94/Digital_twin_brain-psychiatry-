import os
import shutil
import argparse
import time


def get_args():
    parser = argparse.ArgumentParser(description="PyTorch Data Assimilation")
    parser.add_argument("--block_path", type=str, default=None)
    parser.add_argument("--ensembles", type=int, default=100)
    parser.add_argument("--dtype", type=str, default="single")
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


def NewDir(filepath):
    '''
    如果文件夹不存在就创建，如果文件存在就清空！
    
    '''
    if not os.path.exists(filepath):
        os.mkdir(filepath)
    else:
        shutil.rmtree(filepath)
        os.mkdir(filepath)
    
    return


def ln(subject,ensembles,dtype):

    single_path = os.path.join(subject, 'module', dtype)
    ensemble_path = os.path.join(subject, 'multi_module', dtype)
    
    NewDir(ensemble_path)
    N = len(os.listdir(single_path))
    computation_start = time.time()
    for i in range(N):
        progress = i / N
        progress_bar(progress, time.time() - computation_start)
        for j in range(ensembles):
            os.system("ln -s %s/block_%d.npz %s/block_%d.npz"%(single_path, i, ensemble_path, j*N+i))
    
    return ensemble_path

if __name__ == "__main__":
    args = get_args()
    ln(args.block_path,args.ensembles, args.dtype)