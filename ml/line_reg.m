function [ w ] = line_reg(X, y, k)
%LINE_REG Summary of this function goes here
%   Detailed explanation goes here
m = size(X, 2)
XT = pinv(X'*X + (10 ^ k) .* eye(m))*X';
w = XT * y;
end

