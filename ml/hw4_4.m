a = 0;
bias = 0
var = 0
xarray = {};
b = 0;
for i = 1 : 1000
    x = (rand(2, 1) -0.5) * 2;
    xarray{i} = x;
    y = sin(x * pi);
    %x = [ones(2,1), x];
    theta = inv(x' * x) * x' * y;
    
    a = a  + theta(1);
    %b = b  + theta(2);
   % var = var + (theta * x(1, :) - 1.4) ^ 2;
    %bias = bias + (y(1) - 1.4) ^ 2;
end
a = a / 1000
b = b / 1000
%test = [ones(1000,1), (rand(1000, 1) -0.5) * 2];
test = (rand(1000, 1) -0.5) * 2;
for i = 1 : 1000
    x = xarray{i};
    y = sin(x * pi);
    %x = [ones(2,1), x];
    theta = inv(x' * x) * x' * y;
   %y = sin(test(:,2) * pi);
   y = sin(test * pi);
    %test(:,2) = test(:,2) .^ 2;
    var = var + mean((test*theta - test * [a]) .^ 2);
    bias = bias + mean((y - test * [a]) .^ 2);
   
end
a
bias = bias / 1000

var = var / 1000