import os
import numpy as np
from nibabel.testing import data_path
import nibabel as nib

if __name__ == '__main__':

    data_path = '/Users/jslecointre/Documents/DataScience/courses/AI_Medical_Images/project/dataset/MICCAI_BraTS_2019_Data_Training/'
    example_filename = os.path.join(data_path, 'BraTS19_2013_8_1_flair.nii')
    img = nib.load(os.path.join(data_path, 'BraTS19_2013_8_1_flair.nii'))
    print(img.shape)

