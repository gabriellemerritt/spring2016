function sk = createSkew(A)
sk = [0 -A(3) A(2); A(3) 0 -A(1);-A(2) A(1) 0];
return
end