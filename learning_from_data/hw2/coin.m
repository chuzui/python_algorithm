total_ein = 0;
N = 10;
inmiss = 0;
miss = 0;
for c = 1:1000
x1 = (rand(1,2) - 0.5) * 2;
x2 = (rand(1,2) - 0.5) * 2;

points = (rand(N,2) - 0.5) * 2;
k = (x1(2) - x2(2)) / (x1(1) - x2(1));
constant = x2(2) - x2(1) * k;
for i = 1:length(points)
    y(i) = points(i,2) - ((points(i,1)) * k + constant);
    if y(i) > 0
        l(i) = +1;
    else
        l(i) = -1;
    end
end

X = [ones(length(points),1), points];
%XT = inv(X'*X)*X';
XT = pinv(X);
w = XT * y';

ein = sum((w' * X' - y) .^ 2) / N ;
total_ein = total_ein + ein;

for j = 1:N
    hvalue = w' * [1, points(j, :)]';
    if sign(y(j)) ~= sign(hvalue)
        inmiss = inmiss + 1;
    end
end

for j = 1:1000
    point = (rand(1,2) - 0.5) * 2;
    yvalue = point(2) - ((point(1)) * k +constant);
    hvalue = w' * [1, point]';
    if sign(yvalue) ~= sign(hvalue)
        miss = miss + 1;
    end
end
end

total_ein / N
inmiss
miss
miss / (N*1000)
