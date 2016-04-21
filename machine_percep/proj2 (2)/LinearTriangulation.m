function X = LinearTriangulation(K,C1,R1,C2,R2,x1,x2)

n = size(x1,1);
P_1 = K*R1*[eye(3) -C1]; 
P_2 = K*R2*[eye(3) -C2];
x_1 = [x1 ones(n,1)];
x_2 = [x2 ones(n,1)];

X = [];
for i = 1:n
    sk1 = createSkew(x_1(i,:));
    sk2 = createSkew(x_2(i,:));
    A = [sk1*P_1; sk2*P_2];
    [~,~,V] = svd(A);
    X(i,:) = (V(:,end)/V(end,end)).';
end