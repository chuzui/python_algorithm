% File: RecognizeActions.m
%
% Copyright (C) Daphne Koller, Stanford Univerity, 2012

function [accuracy, predicted_labels] = RecognizeActions(datasetTrain, datasetTest, G, maxIter)

% INPUTS
% datasetTrain: dataset for training models, see PA for details
% datasetTest: dataset for testing models, see PA for details
% G: graph parameterization as explained in PA decription
% maxIter: max number of iterations to run for EM

% OUTPUTS
% accuracy: recognition accuracy, defined as (#correctly classified examples / #total examples)
% predicted_labels: N x 1 vector with the predicted labels for each of the instances in datasetTest, with N being the number of unknown test instances


% Train a model for each action
% Note that all actions share the same graph parameterization and number of max iterations
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% YOUR CODE HERE
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
K = size(datasetTrain, 2);
LP = {};
LClassProb = {};
LPairProb = {};
for i=1:K
    [LP{i} loglikelihood LClassProb{i} LPairProb{i}] = EM_HMM(datasetTrain(i).actionData, datasetTrain(i).poseData, G, datasetTrain(i).InitialClassProb, datasetTrain(i).InitialPairProb, maxIter);
end
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


% Classify each of the instances in datasetTrain
% Compute and return the predicted labels and accuracy
% Accuracy is defined as (#correctly classified examples / #total examples)
% Note that all actions share the same graph parameterization

accuracy = 0;


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% YOUR CODE HERE
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
totalactionData = datasetTest.actionData;
totalposeData = datasetTest.poseData;
predicted_labels = zeros(length(totalactionData), 1);
N = size(totalposeData, 1);
correct = 0;
for actionDataIndex = 1:length(totalactionData)
    maxLike = -inf;
    maxLabel = 0;
    for actionIndex=1:K
        P = LP{actionIndex};
        ClassProb = LClassProb{actionIndex};
        PairProb = LPairProb{actionIndex};
        actionData = totalactionData(actionDataIndex);
        index = actionData.marg_ind;
        poseData = totalposeData(index,:,:);
        for i=1:length(index)
            for c=1:K
                g = G(:,:);
                log_sum = 0;
                for h=1:size(g, 1)
                    if g(h,1) == 0
                        log_sum = log_sum + lognormpdf(poseData(i, h, 1), P.clg(h).mu_y(c), P.clg(h).sigma_y(c)) ...,
                        + lognormpdf(poseData(i, h, 2), P.clg(h).mu_x(c), P.clg(h).sigma_x(c)) ..., 
                        + lognormpdf(poseData(i, h, 3), P.clg(h).mu_angle(c), P.clg(h).sigma_angle(c));            
                    else
                        pa = g(h, 2);
                        theta = P.clg(h).theta;
                        log_sum = log_sum + lognormpdf(poseData(i, h, 1), sum(theta(c, 1:4) .* [1, reshape(poseData(i, pa, :),1,3)]), P.clg(h).sigma_y(c)) ...,
                        + lognormpdf(poseData(i, h, 2),sum(theta(c, 5:8) .* [1, reshape(poseData(i, pa, :),1,3)]), P.clg(h).sigma_x(c)) ..., 
                        + lognormpdf(poseData(i, h, 3), sum(theta(c, 9:12) .* [1, reshape(poseData(i, pa, :),1,3)]), P.clg(h).sigma_angle(c));
                    end
                end
            logEmissionProb(i,c) = log_sum;
            end

        end
        
        lf = [];
      init_f = struct('var', [1], 'card', [K], 'val', []);
      init_f.val = log(P.c);
      lf = [lf, init_f];
      for j=1:length(actionData.marg_ind)
          f = struct('var', [j], 'card', [K], 'val', []);
          f.val = logEmissionProb(j,:);
          lf = [lf, f];
      end
      for j=1:length(actionData.pair_ind)
          f = struct('var', [j, j+1], 'card', [K, K], 'val', []);
          f.val = log(P.transMatrix(:)');
          lf = [lf, f];
      end
      [M PCalibrated] = ComputeExactMarginalsHMM(lf);
           
       l = PCalibrated.cliqueList(1).val;
       loglikelihood =logsumexp(l);
        
        if loglikelihood > maxLike
            maxLike = loglikelihood;
            maxLabel = actionIndex;
        end
    end
    predicted_labels(actionDataIndex) = maxLabel;
    if maxLabel == datasetTest.labels(actionDataIndex)
        correct = correct + 1;
    end
end
accuracy = correct / length(totalactionData);
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
