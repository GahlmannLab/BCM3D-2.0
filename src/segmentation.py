from tifffile import imread, imwrite
import os
from skimage import filters, measure, morphology
from skimage.morphology import ball

import numpy as np
from PostProcess import cell_limit, postprocess_1, postprocess_2
from GeneralFunctions import img_norm

def segmentation(img,outputDir,filename, dilationSize = 2):
    """
    Input: an image from the NN, dimention should be (z, 2, x, y)
    Output: save the segmented image
    """
    if img is not None:
        x = img
        print(filename)
        """Normailize first channel (distance to nearest cell exterior) [3, 99.5]"""
        x1 = x[:,0,:,:]
        x1_normal = img_norm(x1, 3, 99.5)
        """Normailize second channel (proximity enhanced cell boundary) [3, 99.5]"""
        x2 = x[:,1,:,:]
        x2_normal = img_norm(x2, 3, 99.5)

        """Threshold"""
        # ‘distance to nearest cell exterior’
        thresh_1 = filters.threshold_otsu(x1_normal)
        x_binary_1 = x1_normal > thresh_1

        # ‘distance to nearest cell exterior’ - ‘proximity enhanced cell boundary’
        x_sub = x1_normal - x2_normal
        x_sub[x_sub < 0] = 0
        thresh_2 = filters.threshold_otsu(x_sub)
        x_binary_2 = x_sub > thresh_2

        """Label connected region"""
        x_binary_1 = morphology.binary_erosion(x_binary_1, ball(1))
        x_labels_1 = measure.label(x_binary_1.astype(int), background=0, return_num=False, connectivity=1)
        
        x_labels_1 = morphology.dilation(x_labels_1, ball(1))
        props = measure.regionprops_table(x_labels_1, properties={'label','area'})
        # smallest object size need change according to cell and voxel size (here we use 27 voxels, our voxel is 100nm cube)
        x_labels_1 = morphology.remove_small_objects(x_labels_1, 27)


        """Find parameters for further process"""
        V_max, V_min, upper_solidity = cell_limit(x_labels_1)

        """Postprocess 1 - simple seeded watershed"""
        x_represent = x_binary_2 * x_sub
        max_label_1 = np.amax(x_labels_1)
        # usually min_seed is about half of the smallest object size (27 here)
        x_labels_2 = postprocess_1(x_labels_1, x_represent, max_label_1, V_max, V_min, upper_solidity, min_seed=12)

        """Postprocess 2 - multi-ostu threshold plus seeded watershed"""
        max_label_2 = np.amax(x_labels_2)
        labels_final = postprocess_2(x_labels_2, x_represent, max_label_2, V_max, V_min, upper_solidity, min_seed=12)
        #Usually dilate 1 or 2 voxels
        labels_final = morphology.dilation(labels_final, ball(dilationSize))
        
        """Save output """
        dir = os.path.join(outputDir, 'Seg')
        if not os.path.exists(dir):
            os.mkdir(dir)
        
        Out_filename = os.path.join(dir, filename)
        imwrite(Out_filename, labels_final.astype('uint16'), metadata={'axes': 'ZYX'})
        