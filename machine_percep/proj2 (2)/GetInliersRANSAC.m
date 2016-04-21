function [y1 , y2, idx] = GetInliersRANSAC(x1, x2, iter, epsl)
max_idx = size(x1,1); 
inliers = []; 
test_inliers = []; 
best_inliers = []; 
best_inlier_num = 0; 
for i = 1:iter
    idxs = randi(max_idx,1,8).'; 
    F = EstimateFundementalMatrix(x1(idxs,:), x2(idxs,:)); 
    F = F/F(3,3); 
    for j=1:max_idx
        vec = (F*[x1(j,:) 1].')/norm(F*[x1(j,:) 1].',2); 
         value = abs([x2(j,:) 1]*vec); 
         if(value < epsl) 
             test_inliers = [test_inliers; j]; 
         end
    end
    inliers = test_inliers;
    test_inliers = []; 
    num_inliers = size(inliers,1); 
    if (num_inliers > best_inlier_num)
         best_inlier_num = num_inliers; 
         best_inliers = inliers; 
    end
    inliers = []; 
end

y1 = x1(best_inliers,:); 
y2 = x2(best_inliers,:); 
idx = best_inliers;
return
end