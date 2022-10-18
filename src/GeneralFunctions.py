import numpy as np
from skimage import morphology
from skimage.morphology import ball


def img_norm(img, low_percentile=3, high_percentile=99.5):
    """Normalize image"""
    img_min = np.percentile(img, low_percentile)
    img_max = np.percentile(img, high_percentile)
    img_normal = (img - img_min) / (img_max - img_min)
    img_normal[img_normal < 0] = 0
    img_normal[img_normal > 1] = 1
    return img_normal

def instance_seg(labels, V_min):
    """instance segmentation"""
    max_labels = np.amax(labels)
    labels = morphology.dilation(labels, ball(2))
    labels = morphology.remove_small_objects(labels, min_size=V_min)
    return [labels, max_labels]

def upper_inner_fence(data):
    """Get upper inner fence"""
    q1 = np.percentile(data, 25)
    q3 = np.percentile(data, 75)
    iq = q3-q1
    out = q3 + 1.5 * iq
    return out