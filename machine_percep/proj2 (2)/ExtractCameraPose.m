function [Cset, Rset] = ExtractCameraPose(E)
Cset = cell(4,1); 
Rest = cell(4,1); 
W = [0 -1 0; 1 0 0 ; 0 0 1]; 
[U,S,V] = svd(E); 
 Rset{1} = U*W*V.'; 
 Rset{2} = U*W*V.'; 
 Rset{3} = U*W.'*V.';
 Rset{4} = U*W.'*V.'; 
 Cset{1} = U(:,3);  
 Cset{2} = -U(:,3);  
 Cset{3} = U(:,3);  
 Cset{4} = -U(:,3);  

 
for i = 1:4
%     Cset{i} = -Rset{i}*U(:,3);  
        Cset{i} = Cset{i}*det(Rset{i});
        Rset{i} = Rset{i}*det(Rset{i});
    
end
return 
end