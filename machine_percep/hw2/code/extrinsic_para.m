function [R, t] = extrinsic_para( frame )
% compute camera extrinsic parameters 
%
% Input:
% - frame: frame number  
% Output:
% - R: 3 by 3, camera extrinsic parameters
% - t: 1 by 3, camera extrinsic parameters
% global K; 
% z = norm(inv(K)*K(:,3)); 
% r_1 = (1/z).*inv(K)*K(:,1); 
% r_2 = (1/z).*inv(K)*K(:,2); 
global R_start; 
global R_delta; 
R = R_start; 
if(frame > 1)
    for i = 1:frame
        R = (R_delta)*R;
    end
end 
t = [0,0,0]; 
end