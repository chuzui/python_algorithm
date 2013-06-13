function theta = svm_train(X, y)
	[m d] = size(X);
	H = eye(d);
	f = 0;
	A = -y';
	b = -1 \ X';
	theta = quadprog(H, f, A, b)
end
