function y = predict(x,w)
  % Predicts based on a linear regression model using weights w
  % x must be a matrix, with one input vector per row
  % w must be a column vector of weights
  n = size(x,1);
  y = [ones(n,1) x] * w;
