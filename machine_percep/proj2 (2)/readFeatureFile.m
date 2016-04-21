function [x1,x2,x3,x4] = readFeatureFile(path)
fid = fopen(path); 
M = dlmread(path, ' ',1,0);
X = cell(1,6); 
for n = 1:size(M,1)
  num_matches = M(n,1)- 1
   idxs = M(n,7:3:7+ 2*num_matches)
   for i= 1:num_matches 
     X{idxs(i)} = M(n, 2*(i-1)+7:2+2*(i-1)+7)
     
   end
   break; 
end
   
        
end
fclose(path);
end
