function [img] = Q4( K, frame )
% render synthetic image for 4.2 using given camera intrinsic matrix and
% frame number
%
% Input:
% - K: camera intrinsic matrix
% - pos: double represent camera center position in z axis.
% Output:
% - img: 1080*1920*3 matrix, the output render image
%
    load data.mat;
    img = ones(h, w, 3);
    
    % object 3
    p2d = project(K, points_C);
    color = color_3;
    img = render(img, p2d, polygons_C, color);
    
    % object 1
    p3d = rotate_object(frame, points_A);
    p2d = project(K, p3d);
    color = color_1;
    img = render(img, p2d, polygons_A, color);

    % object 2
    p2d = project(K, points_B);
    color = color_2;
    img = render(img, p2d, polygons_B, color);
end