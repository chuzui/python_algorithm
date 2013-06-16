function [theta k] = perceptron_train(X, y)

N = size(X, 1);
d = size(X, 2);

theta = zeros(d, 1);
X_train = [X];
k = 0;
while true
	isUpdate = false;
	for i = 1:N
		if sign(X_train(i, :) * theta) ~= y(i)
			theta = theta + (y(i) * X_train(i, :))';
			k = k + 1;
			isUpdate = true;
			%break;
		end
	end
	
	if isUpdate == false
		break;
	end	
end

end
