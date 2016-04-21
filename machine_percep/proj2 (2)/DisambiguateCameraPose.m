function[C,R,X0] = DisambiguateCameraPose(Cset,Rset,Xset)
% 12 13 14 23 24 34 
num_cheirality = 0; 
for i = 1:4
    count = 0 ; 
    n = size(Xset{i},1); 
    for j = 1:n
        if((Rset{i}(3,:)*(Xset{i}(j,1:3).' - Cset{i}) > 0)) 
            count = count +1;
        end
    end
    if(count > num_cheirality)
        R = Rset{i};
        C = Cset{i};
        X0= Xset{i};
        num_cheirality = count; 
    end
end
return
end