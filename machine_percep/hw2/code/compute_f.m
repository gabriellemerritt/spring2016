function [ f ] = compute_f( pos )
A_h = 4; 
D_a  = abs(pos - 4); 
imgheight = 400; %pixel height of A1A2

% compute camera focal length using given camera position
%
% Input:
% - pos: 1 by n, each element represent camera center position on the z axis.
% Output:
% - f: 1 by n, camera focal length
f =(imgheight.*D_a)/A_h;
end

