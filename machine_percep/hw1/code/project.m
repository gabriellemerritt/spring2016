function [ p2d ] = project( p3d, f, pos )
% use for compute vertex image position from given vertex 3D position and
% camera focal length and camera position

% Input:
% - p3d: n by 3, 3D vertex position in world coordinate system
% - f: double, camera focal length
% - pos : double, camera center position
% Output:
% - p2d: n by 2, each row represents vertex image position, in pixel unit
global p_x 
global p_y
point_num = size(p3d,1);
X = p3d(:,1); 
Y = p3d(:,2);
Z = p3d(:,3);
%% This seems wrong but everything is shifted to the right if i put px as in optical x center 
% and py as the optical y center 
K =[f 0 p_y; 0  f p_x; 0 0 1]; 

p2d = K*[X Y Z].';
% 
% x = (f .* (X./ pos -Z)) + p_x; 
% y = (f .* (Y./ pos -Z)) + p_y; 
% z = Z - pos; 
% p2d = round([x y]); 
p2d(1,:)  = p2d(1,:)./(Z- pos)'; 
p2d(2,:) = p2d(2,:)./(Z - pos)';
p2d= round(p2d(1:2,:))'; 
end

