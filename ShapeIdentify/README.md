Train a convolutional neural network to classify segmentation objects as rod or non-rod objects (biologically resonable or unreasonable ojects).

shape3D_training.ipynb - train a CNN based human annotated data (a binary 3D image with human annotate it  as rod or non-rod)

extract_objects.ipynd - extract each object from segmentation and save it as a 3D .tif file. 

shape3D_prediction.ipynb -  classify segmentation object as rod or non-rod by using the pretrained CNN.

check_output.ipynb - map the classification result to the PCA map.

