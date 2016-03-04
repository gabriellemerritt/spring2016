function [ p3d_c ] = world2camera( R, t, p3d )
% transform points from 3D world to camera local 
%
% Input:
% - R: 3 by 3, camera extrinsic parameters
% - t: 1 by 3, camera extrinsic parameters
% - p3d: n by 3, 3D vertex position in world coordinate system.
% Output:
% - p3d_new: n by 3, 3D vertex position after rotation
global K; 
% cam_view = K*[eye(3), zeros(3,1)]*[R t'; zeros(1,3) 1]*[p3d ones(size(p3d,1),1)]'; 
cam_view = [R t'; zeros(1,3) 1]*[p3d ones(size(p3d,1),1)]'; 

p3d_c = cam_view(1:3,:).'; 
end