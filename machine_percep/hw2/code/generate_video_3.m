% generate video for 4.3
% complete following function to generate K matrix
alpha = [1,1]; 
principal_point = [1920/2, 1080/2]; 
s = 0; 
global K;
K = intrinsic_para(400, alpha, principal_point, s);
% 
outputVideo = VideoWriter('output_3.avi');
outputVideo.FrameRate = 6;
open(outputVideo);
for i=1:31
    [R,t] = extrinsic_para(i);
    img = Q3(K, R, t);
    writeVideo(outputVideo, img);
end;
 close(outputVideo);