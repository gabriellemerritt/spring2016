% generate video for 4.4
% complete following function to generate K matrix
alpha = [1,1]; 
principal_point = [1920/2, 1080/2]; 
s = 0; 
K = intrinsic_para(400, alpha, principal_point, s);
outputVideo = VideoWriter('output_4.avi');
load('input_R.mat'); 
outputVideo.FrameRate = 6;
open(outputVideo);
for i=1:31
    img = Q4(K, i);
    writeVideo(outputVideo, img);
end;
close(outputVideo);