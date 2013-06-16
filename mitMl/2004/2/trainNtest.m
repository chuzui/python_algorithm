function [trainE, testE, w] = trainNtest(trainX,trainY,testX,testY,var_ratio)
  w = MAPtrain(trainX,trainY,var_ratio);
  trainYpred = predictY(trainX,w);
  trainE = mean((trainY-trainYpred).^2);
  testYpred = predictY(testX,w);
  testE = mean((testY-testYpred).^2);
