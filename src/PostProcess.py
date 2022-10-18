import numpy as np
from skimage import filters, measure, morphology
from skimage.segmentation import watershed
from GeneralFunctions import upper_inner_fence


def seeded_watershed(input_binary, input_represent, t, min_seed):
    
    """
    Seeded watershed to further split undersegmented objects,
    input_binary - binary image of undersegmented objects
    input_represent - intermediate image represent of undersegmented objects
    t - thresh to get seed
    min_seed - minimum seed volume
    
    Returns
    labels - labeled objects after seeded watershed process
    """
    # Generate seed
    seed_binary = input_represent > t
    seed_label = measure.label(seed_binary.astype(int), background=0, return_num=False, connectivity=1)
    
    # Remove seed that are too small
    seed_label = morphology.remove_small_objects(seed_label, min_size=min_seed)
    
    # Apply watershed
    labels_temp = watershed(-input_represent, seed_label, mask=input_binary)
    
    # There may be objects that have no marks especially at high threshold, but
    # we don't want lose these objects
    labels = labels_temp + input_binary
    # relabel
    labels = measure.label(labels, background=0, return_num=False, connectivity=1)
    labels = morphology.remove_small_objects(labels, min_size=min_seed)
    return labels


def combine_labels(labels_remain, labels_postprocess, max_label, V_min):
    
    """
    Add seeded watershed processed objects back to get complete segmentation results,
    labels_remain - objects that don't need seeded watershed process
    labels_process - objects postprocessed by seeded watershed
    max_label - max label of objects in labels_remain
    
    Returns
    labels_combine - labeled objects after combining
    """
    # Ensure postprocess objects will not affect objects that don't need process
    labels_postprocess[labels_postprocess>0] += max_label
    
    # Combine objects
    labels_combine = labels_remain + labels_postprocess
    
    # Relabel
    labels_combine = measure.label(labels_combine, background=0, return_num=False)
    labels_combine = morphology.remove_small_objects(labels_combine, min_size=V_min)
    
    return labels_combine

def cell_limit(input_labels):
    """
    Find cell limits,
    input_labels - labeled objects
    
    Returns
    V_max - Maximum volume
    V_min - Minimum volume
    upper_solidity - upper limit of solidity
    """
    props = measure.regionprops_table(input_labels, properties={'label','area','convex_area'})
    volume = props['area']
    volume_convex = props['convex_area']
    ratio = volume_convex / volume
    upper_solidity = upper_inner_fence(ratio)
    V_max = upper_inner_fence(volume)
    V_min = V_max / 10

    
    return [V_max, V_min, upper_solidity]
    

def cell_filter(input_labels, input_represent, V_max, upper_solidity):
    """
    Find unreasonable cell objects (based on volume and solidity),
    input_labels - labeled objects
    input_represent - intermediate image represent of objects
    V_max - maximum volume 
    upper_solidity: upper limit of solidity

    Returns
    postprocess_bi - binary image of objects need seeded watershed process
    postprocess_represent - intermediate image represent of objects need 
                            seeded watershed process
    labels_remain - objects don't need seeded watershed process
    """
    postprocess_bi = np.zeros_like(input_labels)
    props = measure.regionprops_table(input_labels, properties={'label','area','convex_area'})
    label = props['label']
    volume = props['area']
    volume_convex = props['convex_area']
    ratio = volume_convex / volume
    for i in range(len(label)):
        #process cell have larger volume than V_max or solidity larger than threshold       
        if volume[i] > V_max or ratio[i] > upper_solidity:
            temp = input_labels == label[i]
            input_labels[input_labels == label[i]] = 0 # Remove objects that may need further process
            postprocess_bi += temp.astype(int)
            
    labels_remain = input_labels
    postprocess_represent = input_represent * postprocess_bi
    return [postprocess_bi, postprocess_represent, labels_remain]

def postprocess_1(input_labels, input_represent, max_label, V_max, V_min, upper_ratio, min_seed):
    """
    Process initial labeld objects by cell_filter, seeded_watershed, labels_combine
    
    input_labels - labeled objects
    input_represent - intermediate image represent of objects
    max_label - max label of objects in labels_remain
    V_max - maximum volume
    V_min - minimum volume
    upper_ratio - upper limit of solidity
    min_seed - min size of seed

    Returns
    labels_combine : labeled objects after processing

    """
    postprocess_bi, postprocess_represent, labels_remain = cell_filter(input_labels, input_represent, V_max, upper_ratio)
    labels_postprocess = seeded_watershed(postprocess_bi, postprocess_represent, 0, min_seed)
    labels_combine = combine_labels(labels_remain, labels_postprocess, max_label, V_min)
    return labels_combine

def postprocess_2(input_labels, input_prob, max_label, V_max, V_min, upper_ratio, min_seed):
    """
    Process labeld objects after postprocess_1 by cell_filter, seeded_watershed, labels_combine and
    multiostu
    
    input_labels - labeled objects
    input_represent - intermediate image represent of objects
    max_label - max label of objects in labels_remain
    V_max - maximum volume
    V_min - minimum volume
    upper_ratio - upper limit of solidity
    min_seed - min size of seed

    Returns
    labels_final : finial labeled objects after processing

    """
    
    postprocess_bi_1, postprocess_prob_1, labels_remain_1 = cell_filter(input_labels, input_prob, V_max, upper_ratio)
    
    if np.sum(postprocess_bi_1) > 0:
        # multiotsu get multi thresholds
        thresh_post = filters.threshold_multiotsu(postprocess_prob_1, classes=5)
        # First threshold
        labels_postprocess_1 = seeded_watershed(postprocess_bi_1, postprocess_prob_1, 
                                            thresh_post[-2], min_seed)
    else:
        labels_postprocess_1 = postprocess_bi_1
        
    if np.sum(labels_postprocess_1) > 0:
        # Second threshold
        postprocess_bi_2, postprocess_prob_2, labels_remain_2 = cell_filter(labels_postprocess_1, 
                                                         postprocess_prob_1, V_max, upper_ratio)
        labels_postprocess_2 = seeded_watershed(postprocess_bi_2, postprocess_prob_2, 
                                            thresh_post[-1], min_seed)
    else:
        labels_postprocess_2 = labels_postprocess_1
        labels_remain_2 = labels_postprocess_1
    
    # Combine postprocess labels
    labels_postprocess = labels_remain_2 + labels_postprocess_2
    labels_postprocess = measure.label(labels_postprocess, background=0, return_num=False, connectivity=1)
    # Combine postprocess and remained labels
    labels_final = combine_labels(labels_remain_1, labels_postprocess, max_label, V_min)
    
    return labels_final
    