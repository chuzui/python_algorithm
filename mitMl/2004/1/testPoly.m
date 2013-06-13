function [trainE, testE] = testPoly(x,y,numtrain,deg,var_ratio)
  % Splits the input and tests a polynomial regression model
  [trainE, testE] = testLinear(degexpand(x,deg),y,numtrain,var_ratio);
