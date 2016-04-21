function [ Rs, ts ] = EstimateRt_linear( Hs, K )
% Linear parameter estimation of R and t
%
%   K: a camera calibration matrix. 3 x 3 matrix.
%
%   Hs: a homography from the world to images. 3 x 3 x N matrix, where N is 
%   the number of calibration images. 
%
%   Rs: rotation matrices. 3 x 3 x N matrix, where N is the number of calibration images. 
%
%   ts: translation vectors. 3 x 1 x N matrix, where N is the number of calibration images. 
%

%% Your code goes here.
[~,~,N] = size(Hs);
for n = 1:N
    h1 = Hs(:,1,n);
    h2 = Hs(:,2,n); 
    h3 = Hs(:,3,n);
    z_p = norm(K\h2); 
    r_1 = (1/z_p).*(K\h1); 
    r_2 = (1/z_p).*(K\h2); 
    r_3 = cross(r_1,r_2); 
    t = (1/z_p).*(K\h3); 
    R = [r_1 r_2 r_3];
    % Re orthagonlize R 
    [U,~,V] = svd(R); 
    R_reotho = U*diag([1 1 det(U*V')])*V'; 
    Rs(:,:,n) = R_reotho; 
    ts(:,:,n) = t; 
end
return 
end

