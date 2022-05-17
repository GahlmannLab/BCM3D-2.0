import numpy as np
from skimage import filters, morphology
from skimage.morphology import ball
import os
from tifffile import imread, imwrite
from scipy import ndimage as ndi

"""Load input"""
stacks = []
filenames = []

# input data is groundtruth or mannual annotation
folder = 'Data/Training/GT' # change folder accordingly
for filename in os.listdir(folder):#import input folder
    if filename.endswith('.tif'):
        img = imread(os.path.join(folder, filename))
        if img is not None:
            stacks.append(img)
            filenames.append(filename)
            
"""Processing"""
stack_num = len(stacks)
for k in range(stack_num):
    stack = stacks[k]
    print(filenames[k])
    label = np.unique(stack)
    cell_dist_sum = np.zeros_like(stack).astype(float)
    boundary_dist_sum = np.zeros_like(stack).astype(float)
    neighbor_dist_sum = np.zeros_like(stack).astype(float)
    for i in range(1,len(label)):
        
        #cell distance
        bw_1 = stack==label[i]
        cell_dist = ndi.distance_transform_edt(bw_1)
        cell_dist = cell_dist/np.amax(cell_dist)
        cell_dist_sum += cell_dist

        #broder distance
        bw_2 = bw_1.astype(int)
        boundary_dist = bw_2 - cell_dist
        boundary_dist_sum += boundary_dist
        
        # neighbor distance
        bw_3 = (stack==label[i]) | (stack == 0)
        neighbor_dist = ndi.distance_transform_edt(bw_3)
        mask = stack == label[i]
        neighbor_dist = mask * neighbor_dist
        neighbor_dist[neighbor_dist==0] = 1e-4 # need caculate 1/x, so replace 0 with a small number
        neighbor_dist = np.reciprocal(neighbor_dist)
        neighbor_dist[neighbor_dist>1] = 0 
        neighbor_dist_sum += neighbor_dist

    # further process
    # distance to nearest cell exterior
    cell_dist_sum = cell_dist_sum ** 3
    cell_dist_sum = 255 * cell_dist_sum
    cell_dist_sum = filters.gaussian(cell_dist_sum, sigma=1) #Gauss blur
    
    # proximity enhanced cell boundary
    neighbor_dist_sum = neighbor_dist_sum/np.amax(neighbor_dist_sum)
    
    boundary_dist_sum = boundary_dist_sum * neighbor_dist_sum 
    boundary_dist_sum = morphology.closing(boundary_dist_sum, ball(2))
    boundary_dist_sum = 255 * boundary_dist_sum
    boundary_dist_sum = filters.gaussian(boundary_dist_sum, sigma=1)
        
    """Output"""
    
    output = np.stack((cell_dist_sum, boundary_dist_sum),axis=-1)
    output = np.moveaxis(output, [0,1,2,3], [-4,-2,-1,-3]) #output need to be ('ZCXY')
    # save output data
    dir = os.path.join('Data/Training/', 'ImageRepresentation')
    if not os.path.exists(dir):
        os.mkdir(dir)
    Out_filename = filenames[k]
    Out_filename = os.path.join(dir, Out_filename)
    imwrite(Out_filename, output.astype('uint8'), imagej=True, metadata={'axes': 'ZCYX'})
        
        
        
        
        