function error = perceptron_test(theta, X test, y test)
	[m, d] = size(X_test);
y_pred = sign(X_test*theta);
test_err = sum(abs(sign(y_test - y_pred)))/m;
end
