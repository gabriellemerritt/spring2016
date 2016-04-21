function [C,R reconstX] = sfm_test(x1, x2, K)
epsl = 1e-4; 
iter = 2000;
[x1, x2] = GetInliersRANSAC(x1,x2, iter, epsl); 
F = EstimateFundementalMatrix(x1,x2); 
E = EssentialMatrixFromFundamentalMatrix(F,K); 
[Cset, Rset] = ExtractCameraPose(E); 
Xset = cell(4,1); 
for i = 1:4
    Xset{i} = LinearTriangulation(K, zeros(3,1), eye(3), Cset{i}, Rset{i},x1,x2);
end
[C, R, X0] = DisambiguateCameraPose(Cset, Rset, Xset);
if det(R) ~= 1
    disp(R); 
end
reconstX = X0; 
return 
end 