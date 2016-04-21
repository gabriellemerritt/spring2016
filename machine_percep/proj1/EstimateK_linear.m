function [K, Hs] = EstimateK_linear(x, X)
% Linear parameter estimation of K
%
%   x:  2D points. n x 2 x N matrix, where n is the number of corners in
%   a checkerboard and N is the number of calibration images
%       
%   X:  3D points. n x 2 matrix, where n is the number of corners in a
%   checkerboard and assumes the points are on the Z=0 plane
%
%   imgs: calibration images. N x 1 cell, where N is the number of calibration images
%
%   K: a camera calibration matrix. 3 x 3 matrix.
%
%   Hs: a homography from the world to images. 3 x 3 x N matrix, where N is 
%   the number of calibration images. You can use est_homography.m to
%   estimate homographies.
%K^-T K^-1 = B 
%% Your code goes here
[~, ~, N] = size(x); 
Hs = zeros(3,3,N);
A = []; 
for n = 1:N
    x_temp = x(:,:,n); 
    x_to = x_temp(:,1); 
    y_to = x_temp(:,2); 
    X_from = X(:,1); 
    Y_from = X(:,2); 
    H = est_homography(x_to, y_to, X_from, Y_from);
%   H = est_homography(y_to, x_to, Y_from,X_from);
%   H = est_homography(X_from, Y_from, x_to, y_to);
%   H = est_homography(Y_from, X_from, y_to, x_to);
    v_11 = calc_v(H,1,1); 
    v_12 = calc_v(H,1,2); 
    v_22 = calc_v(H,2,2);
    A = [A; v_11 - v_22; v_12]; 
    Hs(:,:,n) = H; 
end
[~,~,V] = svd(A); 
b = V(:,end);
B = zeros(3,3); 
B(1,1) = b(1);
B(1,2) = b(2); 
B(1,3) = b(4); 
B(2,2) = b(3); 
B(2,3) = b(5); 
B(3,3) = b(6);
py = (B(1,2)*B(1,3) - B(1,1)*B(2,3))/(B(1,1)*B(2,2) - B(1,2)^2); 
% sorry this  is annoying but i haven't converted this over yet 
%% b vector = [B11 B12 B22 B13 B23 B33] 
c  = B(3,3) -(B(1,3)^2 + py*(B(1,2)*B(1,3) - B(1,1)*B(2,3)))/B(1,1); 

fy = sqrt(c*B(1,1)/(B(1,1)*B(2,2) - B(1,2)^2)); 
fx = sqrt(c/B(1,1));
s = - B(1,2)*fx^2*fy/c; 
px = (s*py/fy)  - (B(1,3)*fx^2/c); 
K  = [ fx s px;...
       0 fy py;...
       0 0 1]; 

end