function [trainE, testE] = trainNtest(trainX,trainY,testX,testY,var_ratio)
  w = MAPtrain(trainX,trainY,var_ratio)
  trainYpred = predict(trainX,w);
  trainE = mean((trainY-trainYpred).^2);
  testYpred = predict(testX,w);
  testE = mean((testY-testYpred).^2);
