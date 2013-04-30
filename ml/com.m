function [ re ] = com(N, v)
%COM Summary of this function goes here
%   Detailed explanation goes here

re = 0;
for i = 0:min(N,v)
    re = re + nchoosek(N, i);
end
end

