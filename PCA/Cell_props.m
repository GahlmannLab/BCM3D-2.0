% extract cellular properties from segmentation result

% change input file accordingly
img = loadtiff('Data\ForSegmentation\Predict\Segmentation\ShewanellaBiofilm\seg_model_Cell_Broder_residual_dist3D0410_Shewanella_488_cytosol&membrane_BgFilter64_11_crop5ms-2.tif');

prop =  regionprops3(img, 'Volume','Solidity','PrincipalAxisLength','EigenVectors','BoundingBox');
Volume = prop.Volume;
Solidity = prop.Solidity;
PrincipalAxisLength_1 = prop.PrincipalAxisLength(:,1);
PrincipalAxisLength_2 = prop.PrincipalAxisLength(:,2);
PrincipalAxisLength_3 = prop.PrincipalAxisLength(:,3);
PrincipalAxisLength_32ratio = prop.PrincipalAxisLength(:,3)./prop.PrincipalAxisLength(:,2);
OrientationVector_x = zeros(length(Volume),1);
OrientationVector_y = zeros(length(Volume),1);
OrientationVector_z = zeros(length(Volume),1);
BoundingBox_x = zeros(length(Volume),1);
BoundingBox_y = zeros(length(Volume),1);
BoundingBox_z = zeros(length(Volume),1);
BoundingBox_wx = zeros(length(Volume),1);
BoundingBox_wy = zeros(length(Volume),1);
BoundingBox_wz = zeros(length(Volume),1);
for i=1:length(Volume)
    OrientationVector_x(i) = prop.EigenVectors{i}(1,1);
    OrientationVector_y(i) = prop.EigenVectors{i}(1,2);
    OrientationVector_z(i) = prop.EigenVectors{i}(1,3);
    BoundingBox_x(i) = prop.BoundingBox(i,1);
    BoundingBox_y(i) = prop.BoundingBox(i,2);
    BoundingBox_z(i) = prop.BoundingBox(i,3);
    BoundingBox_wx(i) = prop.BoundingBox(i,4);
    BoundingBox_wy(i) = prop.BoundingBox(i,5);
    BoundingBox_wz(i) = prop.BoundingBox(i,6);
end


T = table(Volume, Solidity, PrincipalAxisLength_1, PrincipalAxisLength_2, PrincipalAxisLength_3, PrincipalAxisLength_32ratio, ...
    OrientationVector_x, OrientationVector_y, OrientationVector_z, BoundingBox_x, BoundingBox_y, ...
    BoundingBox_z, BoundingBox_wx, BoundingBox_wy, BoundingBox_wz);
% save cellular properties as .csv file
writetable(T,'Data\ShapeIdentify\PCA\ShewanellaBiofilm\ShewanellaBiofilm.csv','Delimiter',',','QuoteStrings',true)

