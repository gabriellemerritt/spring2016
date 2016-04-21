function E = EssentialMatrixFromFundamentalMatrix(F, K)
Ess = K.'*F*K; 
[U,S,V] = svd(Ess);
E = U*[1 0 0 ; 0 1 0; 0 0 0]*V.'; 
return 
end