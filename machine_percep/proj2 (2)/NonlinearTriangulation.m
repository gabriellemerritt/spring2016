
function X = NonlinearTriangulation(K,C1,R1,C2,R2,x1,x2,X0)

params0 = encodeParams(ks_init, K_init, Rs_init, ts_init);
opts = optimoptions(@lsqnonlin, 'Algorithm', 'levenberg-marquardt', 'TolX', 1e-64, 'TolFun', 1e-64, 'MaxFunEvals', 1e64, 'MaxIter',1e3, 'Display', 'iter');
solved_params = lsqnonlin(@(params)GeoError_cb(params,x,X), params0,[],[],opts); 


end

function f = nonlin_error(X,K,R,C)
eus = @(XI,XJ) (bsxfun(@minus,XI,XJ).^2);
n = size(X,1);
uvw = K*R*[eye(3) -C]*[X.';ones(1,n)];
u = uvw(1,:)./uvw(3,:);
v = uvw(2,:)./uvw(3,:);


end
