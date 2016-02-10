function [ p2d ] = project( p3d, f, pos )
% use for compute vertex image position from given vertex 3D position and
% camera focal length and camera position

% Input:
% - p3d: n by 3, 3D vertex position in world coordinate system
% - f: double, camera focal length
% - pos : double, camera center position
% Output:
% - p2d: n by 2, each row represents vertex image position, in pixel unit

point_num = size(p3d,1);
X = p3d(:,1); 
Y = p3d(:,2);
Z = p3d(:,3);
p_x = 1080/2; 
p_y = 1920/2;
K = [f 0 p_x; 0 f p_y; 0 0 1]*[eye(3) zeros(3,1)];
p2d = K*[X Y Z ones(point_num,1)];
p2d = p2d./pos; 


end

