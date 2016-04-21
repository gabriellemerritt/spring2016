function [error, f] = GeoError(x, X, ks, K, Rs, ts)
% Measure a geometric error
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
eus = @(XI,XJ) (bsxfun(@minus,XI,XJ).^2);
error = []; 
f = []; 
%% Your code goes here
[~,~,N] = size(Rs); 
for n = 1:N
Rt = [Rs(:,1:2,n) ts(:,:,n)];
Rt = Rt/Rt(3,3);
uv_reproj =  K*Rt* [X';ones(1,size(X,1))];
uv = uv_reproj(1:2,:);  
x_img = x(:,:,n);
x_img = x_img.';
error = [error;bsxfun(eus,x_img(:) ,uv(:))]; 
f = [f;(x_img - uv).']; 
end



end