import os
import argparse
from os.path import expanduser
import numpy as np
import configparser
import shutil



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
                os.symlink('{0}/{1}'.format(src, file), '{0}/{1}'.format(dst_prefix, file))


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

    train_hgg_dir = [hgg[idx] for idx in train_hgg_idx]
    test_hgg_dir = [hgg[idx] for idx in test_hgg_idx]
    train_lgg_dir = [lgg[idx] for idx in train_lgg_idx]
    test_lgg_dir = [lgg[idx] for idx in test_lgg_idx]

    print('Size of TRAIN dataset : HGG => {0}  LGG => {1}'.format(len(train_hgg_dir), len(train_lgg_dir)))
    print('Size of TEST dataset : HGG => {0}  LGG => {1}'.format(len(test_hgg_dir), len(test_lgg_dir)))

    create_symlinks(train_hgg_dir, test_hgg_dir, train_lgg_dir, test_lgg_dir)

    filename = 'whole_tumor_axial.ini.template'

    config_templates_dir = '{0}/ini_files/{1}'.format(os.getcwd(), filename)
    config_dir = '{0}/niftynet/extensions/{1}'.format(expanduser('~'), modelname)

    config = configparser.ConfigParser()
    config.read_file(open(config_templates_dir))

    for section in ['t1', 't2', 't1ce', 'flair', 'label']:
        config.set(section, 'path_to_search', '{0}/dataset/HGG_train ,{0}/dataset/LGG_train  '.format(os.getcwd()))

    # Writing our configuration file to 'filename.ini'
    with open(config_dir+'/'+filename[:-9], 'w+') as configfile:
        config.write(configfile)
