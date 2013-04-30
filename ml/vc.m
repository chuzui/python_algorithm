function [ p ] = vc( N, dc )
%VC Summary of this function goes here
%   Detailed explanation goes here
sumVc = 0;
for i = 0:dc
    sumVc = sumVc + nchoosek(2*N, i);
end
p = (8 / N * log(4 * (sumVc) / 0.05)) ^ 0.5;

end

