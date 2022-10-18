from tifffile import imread, imwrite
import os
from skimage import filters,morphology
from skimage.morphology import square
import numpy as np

# Substract background
folder = 'G:/20220322_YW_shewan_30c_correctLMMedium+4mmLactate_open/p3_3D/matlab_decon_1/drift_corrected'
for rawfilename in os.listdir(folder):#import raw data folder
    if rawfilename.endswith('.tif') or rawfilename.endswith('.tiff'):
        rawstack = imread(os.path.join(folder, rawfilename))
        if rawstack is not None:
            print(rawfilename)
            stack_size = rawstack.shape
            bg = np.zeros_like(rawstack)
            for z in range(stack_size[0]):
                bg_slice = morphology.opening(rawstack[z,:,:], square(64))
                bg[z,:,:] = filters.median(bg_slice)
            diff = rawstack - bg
            diff[diff<0] = 0
            dir = os.path.join(folder,'PreProcess')
            if not os.path.exists(dir):
                os.mkdir(dir)
            Out_filename = '%s_%s' % ('BgFilter64', rawfilename)
            Out_filename = os.path.join(dir, Out_filename)
            imwrite(Out_filename, diff.astype('uint16'), metadata={'axes': 'ZYX'})