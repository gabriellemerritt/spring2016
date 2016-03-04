function [img] = Q1( K, pos )
% render synthetic image for 4.1 using given camera intrinsic matrix and 
% position
%
% Input:
% - K: 3 by 3, camera intrinsic matrix
% - pos: double, represent camera center position in z axis.
% Output:
% - img: 1080*1920*3 matrix, the output render image
%
% after runing Dolly_Zoom
% you can use 'imwrite(img, 'output.png');' to save the image.

    load data.mat;
    img = ones(h, w, 3);
    
    % object 3
    points_C(:,3) = points_C(:,3) - ones(size(points_C,1),1)*pos;
    p2d = project(K, points_C);
    color = color_3;
    img = render(img, p2d, polygons_C, color);
    
    % object 1
    points_A(:,3) = points_A(:,3) - ones(size(points_A,1),1)*pos;
    p2d = project(K, points_A);
    color = color_1;
    img = render(img, p2d, polygons_A, color);

    % object 2
    points_B(:,3) = points_B(:,3) - ones(size(points_B,1),1)*pos;
    p2d = project(K, points_B);
    color = color_2;
    img = render(img, p2d, polygons_B, color);
end