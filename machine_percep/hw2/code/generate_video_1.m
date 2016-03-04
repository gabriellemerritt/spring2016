% generate video for 4,1
pos = 0:-0.1:-30;
f = compute_f(pos);
alpha = [1,1]; 
principal_point = [1920/2, 1080/2]; 
s = 0; 
outputVideo = VideoWriter('output_1.avi');
outputVideo.FrameRate = 30;
open(outputVideo);
for i=1:size(pos,2)
    % complete following function to generate K matrix
    K = intrinsic_para(f(i), alpha, principal_point, s);  
    img = Q1(K, pos(i));
    writeVideo(outputVideo, img);
end;
 close(outputVideo);