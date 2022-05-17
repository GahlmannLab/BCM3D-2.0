## Network train

1 Use **IntermediateImageGenerate** to generate image representations from groundtruth cell arrangement.

2 Use **TrainingDateGenerate** to generate training pairs (raw data and the corresponding image representations).

3 Use **NetworkTraining** to train CNNs that will transfer input raw data into the corresponding image representations.

## Network predict

1 Use **PreProcessing** to apply background substraction to raw data. (optional)

2 Use **NetworkPredict** to transfer input raw data into image representations.

## Segmentation generate

1 Use **Segmentation** to obtain segmentation result from the predicted image representations.

## Result evaluation

1 Use **PCA** to visualize morphology properties of the segmented objects.

2 Use **ShapeIdentify** to judge whether the segmented objects is biological reasonable.