function [ p2d ] = project( K, p3d )
% use for compute vertex image position from given vertex 3D position and
% camera focal length and camera position

% Input:
% - p3d: n by 3, 3D vertex position in world coordinate system
% -	K: 3*3 matrix, intrinsic K matrix	   
% Output:
% - p2d: n by 2, each row represents vertex image position, in pixel unit
p = K*p3d.';
for i = 1:size(p,2)
    p2d(i,:) = [p(1,i)/p(3,i) p(2,i)/p(3,i)]; 
end 

end

