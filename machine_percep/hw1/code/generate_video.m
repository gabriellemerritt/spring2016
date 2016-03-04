% generate video for Dolly Zoom
 global A_h 
 global C_h
 global a_h 
 global c_h
A_h = 4; 
C_h = 6;

global f_0; 
global K; 
global p_x; 
global p_y; 
f_0 = 400; 
p_x = 1920/2; 
p_y = 1080/2;
K =  [f_0, 0, p_x; ...
      0 , f_0 , p_y; ...
      0 0 1];
a_h = f_0*A_h/p_y; %pixel height in frame 1 
c_h = f_0*C_h/p_y; %pixels
pos = 0:-0.1:-50;
f = compute_f(pos);
figure 
hold on 
outputVideo = VideoWriter('output.avi');
outputVideo.FrameRate = 30;
open(outputVideo);
for i=1:size(pos,2)
    [img, p2d] = Dolly_Zoom(f(i), pos(i));
%      test(i,:) = p2d(:,1).';
     imshow(img);
     writeVideo(outputVideo, img);
end;
close(outputVideo);