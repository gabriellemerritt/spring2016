function [ p3d_new ] = rotate_world( frame, p3d )
% rotate the 3D points about y axis
%
% Input:
% - frame: frame number  
% - p3d: n by 3, 3D vertex position in world coordinate system.
% Output:
% - p3d_new: n by 3, 3D vertex position after rotation
global R_start; 
global R_delta; 
world_points = p3d.';
R = R_start; 
if(frame > 1)
    for i = 1:frame
        R = (R_delta)*R;
    end
end
rotate_world_points = R*world_points; 
p3d_new = rotate_world_points.'; 

end