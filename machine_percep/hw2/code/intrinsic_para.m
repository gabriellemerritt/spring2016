function [ K ] = intrinsic_para( f, alpha, principal_point, s)
% intrinsic_para
%   input:
%       f: double, focal length
%       alpha: 1*2 vector, pixel scale
%       principal_point: 1*2 vector, principal point position
%       s: double, slant factor
%   output:
%       K: 3*3 matrix, intrinsic K matrix
    K  = [ alpha(1)*f s principal_point(1); ...
           0 f*alpha(2) principal_point(2);  ...
           0  0 1]; 

end

