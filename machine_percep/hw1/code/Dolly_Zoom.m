function [img,p2d] = Dolly_Zoom( f, pos )
% render synthetic image using given camera focal length and camera
% position
%
% Input:
% - f: double camera focal length
% - pos: double represent camera center position in z axis.
% Output:
% - img: 1080*1920*3 matrix, the output render image
%
% after runing Dolly_Zoom
% you can use 'imwrite(img, 'output.png');' to save the image.

    load data.mat;
    load points.mat;
    img = ones(h, w, 3);
    
    % object 3
    p2d = project(points_C, f, pos);
    color = color_3;
    img = render(img, p2d, polygons_C, color);
%     img = [];
%     % object 1
    p2d = project(points_A, f, pos);
    color = color_1;
    img = render(img, p2d, polygons_A, color);

    % object 2
    p2d = project(points_B, f, pos);
    color = color_2;
    img = render(img, p2d, polygons_B, color);
end