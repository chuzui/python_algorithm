N = 10;
eta = 0.01;
epochs = 0;
error = 0;
for i = 1:100
    x1 = (rand(1,2) - 0.5) * 2;
    x2 = (rand(1,2) - 0.5) * 2;
    points = (rand(N,2) - 0.5) * 2;
    k = (x1(2) - x2(2)) / (x1(1) - x2(1));
    constant = x2(2) - x2(1) * k;
    for j = 1:length(points)
        y(j) = points(j,2) - ((points(j,1)) * k + constant);
        l(j) = log(y(j));
        if y(j) > 0
            l(j) = 1;
        else
            l(j) = 0;
        end
    end
    
    w = zeros(3,1);
    old_w = ones(3,1);
    while true

        if sum(abs(w-old_w)) < 0.01
            break
        end
        old_w = w;
        for m = randperm(N)
            p = [1, points(m, :)];
            w = w + (eta * (l(m) - (1 / (1 + exp(-w'*p')))) .* p)';
        end
        epochs = epochs + 1;
    end
    
    for i = 1:1000
        point = (rand(1,2) - 0.5) * 2;
        yvalue = point(2) - ((point(1)) * k +constant);
        hvalue = w' * [1, point]';
        if sign(yvalue) ~= sign(hvalue)
            error = error + 1;
        end

    end
end
epochs / 100
error / 100