function [C R] = LinearPnP(X,x,K)
n = size(X,1); 
A = [] 
X_h = X;
u = x(:,1); 
v = x(:,2); 
for i = 1:n
    A = [A; zeros(1,4) -X_h(i,:) v(i)*X_h(i,:); ... 
        X_h(i,:) zeros(1,4) -u(i)*X_h(i,:); ... 
        -v(i)*X_h(i,:) u(i)*X_h(i,:) zeros(1,4)]; 
end
[U,S,V] = svd(A); 
P = V(:,end)/V(end,end); 
P=reshape(P,3,4);

end