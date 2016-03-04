% generate video for 4.2
% complete following function to generate K matrix
% f = compute_f(pos);
alpha = [1,1]; 
principal_point = [1920/2, 1080/2]; 
s = 0; 
K = intrinsic_para(400, alpha, principal_point, s);
load('input_R.mat'); 
% global R_delta; 
% global R_start; 
outputVideo = VideoWriter('output_2.avi');
outputVideo.FrameRate = 6;
open(outputVideo);
for i=1:31
    fprintf('DEBUG:FRAME %d', i); 
    img = Q2(K, i);
%     hold on 
    writeVideo(outputVideo, img);
end
close(outputVideo);