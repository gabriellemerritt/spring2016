function [img] = Q3( K, R, t )
% render synthetic image for 4.4 using given camera intrinsic matrix and
% frame number
%
% Input:
% - K: camera intrinsic matrix
% - R: 3 by 3, camera extrinsic parameters
% - t: 1 by 3, camera extrinsic parameters
% Output:
% - img: 1080*1920*3 matrix, the output render image
%
    load data.mat;
    img = ones(h, w, 3);
    
    % object 3
    p3d = world2camera(R, t, points_C);
    p2d = project(K, p3d);
    color = color_3;
    img = render(img, p2d, polygons_C, color);
    
    % object 1
    p3d = world2camera(R, t, points_A);
    p2d = project(K, p3d);
    color = color_1;
    img = render(img, p2d, polygons_A, color);

    % object 2
    p3d = world2camera(R, t, points_B);
    p2d = project(K, p3d);
    color = color_2;
    img = render(img, p2d, polygons_B, color);
end