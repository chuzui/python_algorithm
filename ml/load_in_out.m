in = load('in.dta');
out = load('out.dta');
x1 = in(:, 1);
x2 = in(:, 2);

x_in = [ones(length(in), 1), x1, x2, x1 .^ 2, x2 .^ 2, x1 .* x2, abs(x1-x2), abs(x1+x2)];
y_in = in(:, 3);

x1 = out(:, 1);
x2 = out(:, 2);
x_out = [ones(length(out), 1), x1, x2, x1 .^ 2, x2 .^ 2, x1 .* x2, abs(x1-x2), abs(x1+x2)];
y_out = out(:, 3);