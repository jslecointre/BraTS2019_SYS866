import os
import argparse
from os.path import expanduser
import numpy as np
import configparser
import shutil
import pandas as pd



def get_file_names(dataset_path):
    """
    get_file_names(str) -> list of HGG files , LGG files

    It return the paths of the LGG and HGG files present in BraTS dataset
    """
    
    lgg_dir = []
    hgg_dir = []

    for r, d, f in os.walk(dataset_path):
        if 'LGG' in r:
            for folder in d:
                lgg_dir.append(os.path.join(r, folder))
        elif 'HGG' in r:
            for folder in d:
                hgg_dir.append(os.path.join(r, folder))
    return lgg_dir, hgg_dir


def get_rdm_indexes(ratio, length):

    indexes = np.arange(0, length)
    # shuffle
    np.random.seed(seed=42)
    np.random.shuffle(indexes)
    return indexes[int(ratio * length):], indexes[:int(ratio * length)]


def create_symlinks(tr_hgg, te_hgg, tr_lgg, te_lgg):

    cwd = os.getcwd()
    dir_contents = dict(zip(['HGG_train', 'HGG_test', 'LGG_train', 'LGG_test'], [tr_hgg, te_hgg, tr_lgg, te_lgg]))

    # for dataset type train test LGG or HGG
    for d, sub_dirs in dir_contents.items():
        dst_prefix = '{0}/dataset/{1}'.format(cwd, d)

        shutil.rmtree(dst_prefix)
        os.makedirs(dst_prefix)

        # for each directory (patient)
        for src in sub_dirs:

            all_files = os.listdir(src)
            # for each file type per patient (t1,t2,t1ce,flair,seg)
            for file in all_files:
                #print('{0}/{1}'.format(src, file))
                os.symlink('{0}/{1}'.format(src, file), '{0}/{1}'.format(dst_prefix, file))


def create_symlinks_all_data(hgg, lgg):

    cwd = os.getcwd()
    dir_contents = dict(zip(['HGG', 'LGG'], [hgg, lgg]))

    # for dataset type train test LGG or HGG
    for d, sub_dirs in dir_contents.items():
        dst_prefix = '{0}/dataset/{1}'.format(cwd, d)

        shutil.rmtree(dst_prefix)
        os.makedirs(dst_prefix)

        # for each directory (patient)
        for src in sub_dirs:

            all_files = os.listdir(src)
            # for each file type per patient (t1,t2,t1ce,flair,seg)
            for file in all_files:
                #print('{0}/{1}'.format(src, file))
                os.symlink('{0}/{1}'.format(src, file), '{0}/{1}'.format(dst_prefix, file))
                print('src', '{0}/{1}'.format(src, file))
                print('dst', '{0}/{1}'.format(dst_prefix, file))


def create_symlinks_gt_brats(hgg, lgg ,year=17):

    #cwd = os.getcwd()
    dir_contents = dict(zip(['HGG', 'LGG'], [hgg, lgg]))

    dest_dir = '/mnt/SYS866/data/gt{0}'.format(year)

    # for dataset type train test LGG or HGG
    for d, sub_dirs in dir_contents.items():
        dst_prefix = '{0}/{1}'.format(dest_dir, d)

        shutil.rmtree(dst_prefix)
        os.makedirs(dst_prefix)

        # for each directory (patient)
        for src in sub_dirs:

            all_files = os.listdir(src)
            dst_folder = dst_prefix + '/{0}'.format(src.split('/')[-1])
            print(dst_folder)
            os.makedirs(dst_folder)
            # for each file type per patient (t1,t2,t1ce,flair,seg)
            for file in all_files:
                #print('{0}/{1}'.format(src, file))
                if 'seg' in file:
                    os.symlink('{0}/{1}'.format(src, file), '{0}/{1}'.format(dst_folder, file))
                    print('src', '{0}/{1}'.format(src, file))
                    print('dst', '{0}/{1}'.format(dst_folder, file))


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset_dir", type=str, default="mnt/dataset/MICCAI_BraTS_2019_Data_Training/", help="path to dataset")
    parser.add_argument("--model_name", type=str, default="anisotropic_nets_brats_challenge", help="niftynet model name to use")

    opt = parser.parse_args()
    print(opt)

    data_dir = opt.dataset_dir
    modelname = opt.model_name

    lgg, hgg = get_file_names(data_dir)
    test_ratio = 0.1

    train_hgg_idx, test_hgg_idx = get_rdm_indexes(test_ratio, len(hgg))
    train_lgg_idx, test_lgg_idx = get_rdm_indexes(test_ratio, len(lgg))

    # for i in [lgg[idx].split('/')[-1] for idx in test_lgg_idx]:
    #     print('{0},inference'.format(i))

    # for i in [hgg[idx].split('/')[-1] for idx in test_hgg_idx]:
    #     print('{0},inference'.format(i))

    # for i in [hgg[idx].split('/')[-1] for idx in test_hgg_idx]:
    #     print('HGG/{0}'.format(i))
    #
    # for i in [lgg[idx].split('/')[-1] for idx in test_lgg_idx]:
    #     print('LGG/{0}'.format(i))

    # for i in [hgg[idx].split('/')[-1] for idx in train_hgg_idx]:
    #     print('HGG/{0}'.format(i))
    test17 = pd.read_csv('patients_in19_not_in17.csv')
    print(test17.columns)

    train19_hgg_dir = [hgg[idx] for idx in train_hgg_idx]
    test19_hgg_dir = [hgg[idx] for idx in test_hgg_idx]
    train19_lgg_dir = [lgg[idx] for idx in train_lgg_idx]
    test19_lgg_dir = [lgg[idx] for idx in test_lgg_idx]

    print('Size of TRAIN dataset : HGG => {0}  LGG => {1}'.format(len(train19_hgg_dir), len(train19_lgg_dir)))
    print('Size of TEST dataset : HGG => {0}  LGG => {1}'.format(len(test19_hgg_dir), len(test19_lgg_dir)))

    #create_symlinks(train_hgg_dir, test_hgg_dir, train_lgg_dir, test_lgg_dir)

    #create_symlinks_all_data(hgg, lgg)

    test17_hgg_dir = [data_dir+x for x in test17.patient_id.values if 'HGG' in x]
    test17_lgg_dir = [data_dir + x for x in test17.patient_id.values if 'LGG' in x]

    create_symlinks_gt_brats(test17_hgg_dir, test17_lgg_dir)
