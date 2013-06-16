function w = MAPtrain(x,y,var_ratio)
  % Train a regularised linear regression model: 
  %   returns the weights w minimizing norm(y-[1 x]*w)
  % x must be a matrix, with one input vector per row
  % y must be a column matrix of output values
  % the returned w is a column vector of weights
  n = size(x,1);
  X=[ones(n,1) x];
  
  w=pinv(X'*X+var_ratio*eye(size(X,2)))*X'*y;
  %w = pinv([ones(n,1) x])*y;