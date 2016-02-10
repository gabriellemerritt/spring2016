% generate video for Dolly Zoom
pos = 0:-0.1:-50;
f = compute_f(pos);

outputVideo = VideoWriter('output.avi');
outputVideo.FrameRate = 30;
open(outputVideo);
for i=1:size(pos,2)
    img = Dolly_Zoom(f(i), pos(i));
    writeVideo(outputVideo, img);
end;
close(outputVideo);