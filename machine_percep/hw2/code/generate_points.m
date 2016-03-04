% generate vertexs 3D position
load start.mat
f = 400;

points_A = unproject(A_p, A_d, f);
points_B = unproject(B_p, B_d, f);
points_C = unproject(C_p, C_d, f);

save 'points.mat' points_A points_B points_C