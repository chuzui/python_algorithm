function w = train(x,y)
  % Train a linear regression model: 
  %   returns the weights w minimizing norm(y-[1 x]*w)
  % x must be a matrix, with one input vector per row
  % y must be a column matrix of output values
  % the returned w is a column vector of weights
  n = size(x,1);
  w = pinv([ones(n,1) x])*y;