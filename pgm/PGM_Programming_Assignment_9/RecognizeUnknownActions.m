% You should put all your code for recognizing unknown actions in this file.
% Describe the method you used in YourMethod.txt.
% Don't forget to call SavePrediction() at the end with your predicted labels to save them for submission, then submit using submit.m
datasetTest3.labels = zeros(90, 1);
datasetTrain3(1).actionData = [datasetTrain1(1).actionData, datasetTrain2(1).actionData, datasetTrain3(1).actionData];
datasetTrain3(1).poseData = [datasetTrain1(1).poseData, datasetTrain2(1).poseData, datasetTrain3(1).poseData];

[accuracy, predicted_labels] = RecognizeActions(datasetTrain3, datasetTest3, G, 10);
SavePredictions(predicted_labels);