function [ p3d_new ] = rotate_object( frame, p3d )
% rotate the 3D points about specific line
%
% Input:
% - frame: frame number  
% - p3d: n by 3, 3D vertex position in world coordinate system.
% Output:
% - p3d_new: n by 3, 3D vertex position after rotation
axis = cross([-2 -2 4],[-2 2 4]);
global R_start; 
global R_delta; 
world_points = [p3d.'; ones(1,size(p3d,1))];
R = R_start; 
if(frame > 1)
    for i = 1:frame
        R = (R_delta)*R;
    end
end
conj_rotation = [R , (eye(3) - R)*[-4,-2,5.].'; 0 0 0 1];
p3d_new =(conj_rotation*world_points).';
p3d_new = p3d_new(:,1:3); 
end