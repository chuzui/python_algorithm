function [trainE,testE] = testLinear(x,y,numtrain,var_ratio)
  % Splits the data to a training set and test sets, and
  % returns the training and test error for linear regression
  
  test_start=250; %only data after this index is used for testing
  
  trainX = x(1:numtrain,:);
  trainY = y(1:numtrain);
  testX = x((test_start+1):end,:);
  testY = y((test_start+1):end);
  [trainE,testE] = trainNtest(trainX,trainY,testX,testY,var_ratio);
