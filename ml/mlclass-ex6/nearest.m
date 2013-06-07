function len = nearest(X)

m = size(X, 1);

len = inf;

for i=1:(m-1)
	for j = (i+1):m
		dis = distance(X(i, :), X(j, :));
		if dis < len
			len = dis;
		end	
	end
end
len = len / log(m - 1);
end

function dis = distance(x1, x2)
	dis = sum((x1 - x2) .^ 2) .^ 0.5;
end
