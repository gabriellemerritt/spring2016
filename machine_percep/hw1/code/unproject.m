function [ p3d ] = unproject( p, d, f )
% compute vertexs 3D position using their image position ,depth and camera
% focal length
% 
% Input:
% - p: n by 2, each row represent vertex image position, in pixel unit
% - d: n by 1, each row represent distance to the $xy$ plane
% - f: double, camera focal length
% Output:
% - p3d: n by 3, vertex position in world coordinate system
% d*[u_img , v_img, 1] = [ ax*fx  s px_0 0 ; 0 ay*fy py_0 0 ;  0 0 1 0]*[R t][X Y Z ]
% u and v are 2d projectives


 num_points = size(p,1); 
  xp = p(:,1); 
  yp = p(:,2); 
  p_x = 1080/2; 
  p_y = 1920/2;
  K = [f, 0, p_x; 0 , f , p_y; 0 0 1] * [eye(3) zeros(3,1)]; 
  
  cam_pos = ((K)\[d.*xp, d.*yp, d.*ones(num_points,1)]');
  x_c = cam_pos(1,:)'; 
  y_c = cam_pos(2,:)';
  z_c = cam_pos(3,:)';
  
  XZ = -x_c;
  YZ = -y_c;
  ZZ = -d;
  p3d = [XZ YZ ZZ]; 
  
  %Assuming no rotation or translation 
  
end

