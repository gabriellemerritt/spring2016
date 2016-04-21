function F = EstimateFundementalMatrix(x1,x2)
%%
% (INPUT) x1 and x2: N×2 matrices whose row represents a correspondence.
% (OUTPUT) F: 3×3 matrix with rank 2.
% The fundamental matrix can be estimated by solving linear least squares (Ax = 0).
%%
A = [];
x_1 = x1(:,1); 
y_1 = x1(:,2); 
x_2 = x2(:,1); 
y_2 = x2(:,2); 
for i=1:size(x1,1)
   A(i,:) = [x_1(i)*x_2(i), x_1(i)*y_2(i), x_1(i) ,y_1(i)*x_2(i), y_1(i)*y_2(i), y_1(i), x_2(i), y_2(i), 1];
end
[u,s,v] = svd(A); 
F = reshape(v(:,end),[3,3]); 
[U,S,V] = svd(F); 
S(3,3) = 0; 
F = U*S*V.';
return 
end