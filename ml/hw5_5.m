function [ count ] = hw5_5()
%HW5_5 Summary of this function goes here
%   Detailed explanation goes here

u = 1;
v = 1;
beta = 0.1;
inte = 1e-14;
count = 0;
for i = 1:15
    e = (u * exp(v) - 2 * v * exp(-u)) ^ 2
    if abs(e) < inte
        break
    end
    oldu = u;
    count = count + 1;
    u = u - 2 * (exp(v) + 2*v*exp(-u)) * (u*exp(v) - 2 * v * exp(-u)) * beta;
    oldu = u;
    v = v - 2 * (oldu*exp(v) - 2 * exp(-oldu)) * (oldu*exp(v) - 2 * v * exp(-oldu)) * beta;
end

count
u
v
e = (u * exp(v) - 2 * v * exp(-u)) ^ 2
end

