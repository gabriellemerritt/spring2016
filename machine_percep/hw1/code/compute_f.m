function [ f ] = compute_f( pos )
% compute camera focal length using given camera position
global C_h
global A_h
global f_0
global a_h
global p_y
A_z = 4;
D_a  = abs(pos - 4); 
pctg = 400/(2*p_y); 


 imgheight = 400; %pixel height of A1A2
% width = 300; 
 f =(imgheight.*D_a)/A_h;
end

