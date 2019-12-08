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
    parser.add_argument("--dataset_dir", type=str, default="mnt/dataset/MICCAI_BraTS_2019_Data_Training/",
                        help="path to dataset")
    parser.add_argument("--model_name", type=str, default="deepmedic",
                        help="niftynet model name to use")

    opt = parser.parse_args()
    print(opt)

    data_dir = opt.dataset_dir
    modelname = opt.model_name

    filename = 'deepmedic_config.ini.template'

    config_templates_dir = '{0}/ini_files/{1}/{2}'.format(os.getcwd(), modelname, filename)
    config_dir = '{0}/niftynet/extensions/{1}'.format(expanduser('~'), modelname)

    config = configparser.ConfigParser()
    config.read_file(open(config_templates_dir))

    all_dataset_directory = ''

    for section in ['t1', 't2', 't1ce', 'flair', 'label']:
        config.set(section, 'path_to_search', '{0}/dataset/HGG ,{0}/dataset/LGG  '.format(os.getcwd()))

    #for section in ['EVALUATION', 'INFERENCE']:
    #    config.set(section, 'path_to_search', '{0}/dataset/HGG ,{0}/dataset/LGG  '.format(os.getcwd()))

    # Writing our configuration file to 'filename.ini'
    with open(config_dir + '/' + filename[:-9], 'w+') as configfile:
        print(config_dir + '/' + filename[:-9])
        config.write(configfile)


