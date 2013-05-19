k = [3,4,5,6,7];
load 'in.dta'
load 'out.dta'
train = in(26:end, :);
valid = in(1:25, :);
addpath 'ex1'
x1 = train(:, 1);
x2 = train(:, 2);
x_in = [ones(   size(x1, 1), 1), x1, x2, x1 .^ 2, x2 .^ 2, x1 .* x2, abs(x1 - x2), abs(x1 + x2)];
y_in = train(:, 3);

%x1 = valid(:, 1);
%x2 = valid(:, 2);
x1 = out(:, 1);
x2 = out(:, 2);
x_out = [ones(size(x1, 1), 1), x1, x2, x1 .^ 2, x2 .^ 2, x1 .* x2, abs(x1 - x2), abs(x1 + x2)];
y_out = out(:, 3);
for i = k
    i
    temp_x_in = x_in(:, 1:i+1);
    w = line_reg(temp_x_in, y_in, 1);
    temp_x_out = x_out(:, 1: i+1);
    computeCost(temp_x_out, y_out, w)
end
