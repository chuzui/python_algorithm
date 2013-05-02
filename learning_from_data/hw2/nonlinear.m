total_ein = 0;
N = 1000;
inmiss = 0;
miss = 0;

w1 = [-1, -0.05, 0.08, 0.13, 1.5, 1.5]
w2 = [-1, -0.05, 0.08, 0.13, 1.5, 15]
w3 = [-1, -0.05, 0.08, 0.13, 15, 1.5]
w4 = [-1, -1.5, 0.08, 0.13, 0.05, 0.05]
w5 = [-1, -0.05, 0.08, 1.5, 0.15, 0.15]
miss1 = 0
miss2 = 0
miss3 = 0
miss4 = 0
miss5 = 0
for c = 1:1000

points = (rand(N,2) - 0.5) * 2;

for i = 1:length(points)
    y(i) = sum(points(i, :) .^2) - 0.6;
    if i < N / 10 && rand() > 0.5
        %y(i) = -y(i);
    end
end

X = [ones(length(points),1), points, points(:, 1) .* points(:, 2), points .^ 2];
XT = inv(X'*X)*X';
w = XT * y';

ein = sum((w' * X' - y) .^ 2) / N ;
total_ein = total_ein + ein;

for j = 1:N
    %hvalue = w' * [1, points(j, :)]';
    hvalue = w' * [1, points(j, :), points(j,1)*points(j,2), points(j,1)^2, points(j,2)^2]';
    if sign(y(j)) ~= sign(hvalue)
        inmiss = inmiss + 1;
    end
end

for j = 1:1000
    point = (rand(1,2) - 0.5) * 2;
    yvalue = sum(point .^2) - 0.6;
    xt = [1, point, point(1)*point(2), point(1)^2, point(2)^2]';
    %hvalue = w' * [1, point]';
    hvalue = w' * xt;
    if sign(yvalue) ~= sign(hvalue)
        miss = miss + 1;
    end
    
    if sign(w1 *xt) ~= sign(hvalue)
        miss1 = miss1 + 1;
    end
    if sign(w2*xt) ~= sign(hvalue)
        miss2 = miss2 + 1;
    end
    if sign(w3*xt) ~= sign(hvalue)
        miss3 = miss3 + 1;
    end
    if sign(w4*xt) ~= sign(hvalue)
        miss4 = miss4 + 1;
    end
    if sign(w5*xt) ~= sign(hvalue)
        miss5 = miss5 + 1;
    end
end
end

total_ein / N
inmiss
miss
miss / (N*1000)

miss1
miss2
miss3
miss4
miss5
