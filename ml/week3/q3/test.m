[X, y, theta_true] = load_data;
size(X);
y;
lambdas = [0.001, 9.01, 0.1, 1, 10];

for i=1:length(lambdas)
	lambda = lambdas(i);
	printf(num2str(lambda));
	theta = l1ls(X,y,lambda);
	theta'
end


