p = (9 + 4 * 6 ^0.5) ^ 0.5;

x = [1 -1;1 p;1 1];
y = [0; 1; 0];
e_cv = 0;
for i = 1:3
    x_in = x;
    x_in(i, :) = [];
    y_in = y;
    y_in(i) = [];
    w = line_reg(x_in, y_in, 1);
    e_cv = e_cv + (x(i, :) * w - y(i)) .^ 2;
end
e_cv