function [ks] = EstimateDistort_linear(x, X, K, Rs, ts)
% Linear parameter estimation of k
%
%   x:  2D points. n x 2 x N matrix, where n is the number of corners in
%   a checkerboard and N is the number of calibration images
%       
%   X:  3D points. n x 2 matrix, where n is the number of corners in a
%   checkerboard and assumes the points are on the Z=0 plane
%
%   K: a camera calibration matrix. 3 x 3 matrix.
%
%   Rs: rotation matrices. 3 x 3 x N matrix, where N is the number of calibration images. 
%
%   ts: translation vectors. 3 x 1 x N matrix, where N is the number of calibration images. 
%
%   ks: radial distortion parameters. 2 x 1 matrix, where ks(1) = k_1 and
%   ks(2) = k_2.
%

%% Your code goes here
% bsxfun(fun,ab(1,:),ab(2,:));
[~,~,N] = size(Rs); 
K_p  = K; 
K_p(1,2) = 0; 
A = [];
b = [];
%% Optical center put into alternating px py for N*num_corners
%  
pxy = K(1:2,3)*ones(1,size(X,1));
pxy = reshape(pxy,2*size(X,1),1);
new_r = ones(2*size(X,1),1);
%% For loop for each image, vectorizes uv_ideal, uv_img, optical center, and r into form from notes
for n = 1:N
    Rt = [Rs(:,1:2,n) ts(:,:,n)];
    ab = Rt* [X';ones(1,size(X,1))]; 
    r = sum(ab(1:2,:).^2);
    new_r(1:2:end) = r;
    new_r(2:2:end) = r;
    uv_ideal =  K_p*Rt* [X';ones(1,size(X,1))];
    % reshapes uv_ideal into alternating u_ideal v_ideal vector for m elements
    uv_i = reshape(uv_ideal(1:2,:),2*size(X,1),1);
    A = [A;(uv_i - pxy).*new_r (uv_i - pxy).*(new_r.^2)];
    uv_img = x(:,:,n);
    uv_img = uv_img.';
    % reshapes uv_img into alternating u_img and v_img
    uv_img = reshape(uv_img,2*size(X,1),1); 
    b = [b; uv_img - uv_i];
end

ks = A\b;
end