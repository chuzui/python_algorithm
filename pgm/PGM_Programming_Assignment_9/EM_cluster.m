% File: EM_cluster.m
%
% Copyright (C) Daphne Koller, Stanford Univerity, 2012

function [P loglikelihood ClassProb] = EM_cluster(poseData, G, InitialClassProb, maxIter)

% INPUTS
% poseData: N x 10 x 3 matrix, where N is number of poses;
%   poseData(i,:,:) yields the 10x3 matrix for pose i.
% G: graph parameterization as explained in PA8
% InitialClassProb: N x K, initial allocation of the N poses to the K
%   classes. InitialClassProb(i,j) is the probability that example i belongs
%   to class j
% maxIter: max number of iterations to run EM

% OUTPUTS
% P: structure holding the learned parameters as described in the PA
% loglikelihood: #(iterations run) x 1 vector of loglikelihoods stored for
%   each iteration
% ClassProb: N x K, conditional class probability of the N examples to the
%   K classes in the final iteration. ClassProb(i,j) is the probability that
%   example i belongs to class j

% Initialize variables
N = size(poseData, 1);
K = size(InitialClassProb, 2);

if size(G, 3) == 1
    G = repmat(G, [1, 1, K]);
end

ClassProb = InitialClassProb;

loglikelihood = zeros(maxIter,1);

P.c = [];
P.clg.sigma_x = [];
P.clg.sigma_y = [];
P.clg.sigma_angle = [];


P.clg = repmat(struct('mu_y', [], 'sigma_y', [], 'mu_x', [], 'sigma_x', [], 'mu_angle', [], 'sigma_angle', [], 'theta', []), 1, 10);
% EM algorithm
for iter=1:maxIter
  
  % M-STEP to estimate parameters for Gaussians
  %
  % Fill in P.c with the estimates for prior class probabilities
  % Fill in P.clg for each body part and each class
  % Make sure to choose the right parameterization based on G(i,1)
  %
  % Hint: This part should be similar to your work from PA8
  
  P.c = zeros(1,K);
  
  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  % YOUR CODE HERE
  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  P.c = sum(ClassProb)/ sum(sum(ClassProb));


for i = 1:10
    if G(i, 1) == 0
        for k=1:K       
            [P.clg(i).mu_y(k) P.clg(i).sigma_y(k)] = FitG(reshape(poseData(:, i, 1), N , 1) , ClassProb(:, k)); 
            [P.clg(i).mu_x(k) P.clg(i).sigma_x(k)] = FitG(reshape(poseData(:, i, 2), N , 1) , ClassProb(:, k)); 
            [P.clg(i).mu_angle(k) P.clg(i).sigma_angle(k)] = FitG(reshape(poseData(:, i, 3), N , 1) , ClassProb(:, k)); 
        end
    else
        for k=1:K
            pa = G(i, 2);

            U = reshape(poseData(:, pa, :), N, 3);
            %Ux = reshape(dataset(find(labels(:, k)), pa, 2), sum(labels(:, k)), 1);
            %Uangle = reshape(dataset(find(labels(:, k)), pa, 3), sum(labels(:, k)), 1);
            
            y = poseData(:, i, 1);
            [Beta P.clg(i).sigma_y(k)] = FitLG(y, U, ClassProb(:, k));
            P.clg(i).theta(k, 1:4) = [Beta(4), Beta(1:3)']; 
            
            x = poseData(:, i, 2);
            [Beta P.clg(i).sigma_x(k)] = FitLG(x, U, ClassProb(:, k));
            P.clg(i).theta(k, 5:8) = [Beta(4), Beta(1:3)']; 
            
            angle = poseData(:, i, 3);
            [Beta P.clg(i).sigma_angle(k)] = FitLG(angle, U, ClassProb(:, k));
            P.clg(i).theta(k, 9:12) = [Beta(4), Beta(1:3)']; 
            %[P.clg(i).mu_y(k) P.clg(i).sigma_y(k)] = FitGaussianParameters(reshape(dataset(find(labels(:, k)), i, 1), sum(labels(:, k)), 1)); 
        end
    end
end
  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  
  % E-STEP to re-estimate ClassProb using the new parameters
  %
  % Update ClassProb with the new conditional class probabilities.
  % Recall that ClassProb(i,j) is the probability that example i belongs to
  % class j.
  %
  % You should compute everything in log space, and only convert to
  % probability space at the end.
  %
  % Tip: To make things faster, try to reduce the number of calls to
  % lognormpdf, and inline the function (i.e., copy the lognormpdf code
  % into this file)
  %
  % Hint: You should use the logsumexp() function here to do
  % probability normalization in log space to avoid numerical issues
  
  ClassProb = zeros(N,K);
  
  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  % YOUR CODE HERE
  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  for i=1:N
    for c=1:K
        g = G(:,:,c);
        log_sum = 0;
        for k=1:size(g, 1)
            if g(k,1) == 0
                log_sum = log_sum + lognormpdf(poseData(i, k, 1), P.clg(k).mu_y(c), P.clg(k).sigma_y(c)) ...,
                + lognormpdf(poseData(i, k, 2), P.clg(k).mu_x(c), P.clg(k).sigma_x(c)) ..., 
                + lognormpdf(poseData(i, k, 3), P.clg(k).mu_angle(c), P.clg(k).sigma_angle(c));            
            else
                pa = g(k, 2);
                theta = P.clg(k).theta;
                log_sum = log_sum + lognormpdf(poseData(i, k, 1), sum(theta(c, 1:4) .* [1, reshape(poseData(i, pa, :),1,3)]), P.clg(k).sigma_y(c)) ...,
                + lognormpdf(poseData(i, k, 2),sum(theta(c, 5:8) .* [1, reshape(poseData(i, pa, :),1,3)]), P.clg(k).sigma_x(c)) ..., 
                + lognormpdf(poseData(i, k, 3), sum(theta(c, 9:12) .* [1, reshape(poseData(i, pa, :),1,3)]), P.clg(k).sigma_angle(c));
            end
        end
        ClassProb(i,c) = log_sum + log(P.c(c));
    end
    %ClassProb(i, :) =  exp(ClassProb(i, :) - logsumexp(ClassProb(i,:)));
end
  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  %ClassProb = logsumexp(ClassProb);
  % Compute log likelihood of dataset for this iteration
  % Hint: You should use the logsumexp() function here
  loglikelihood(iter) = 0;
  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  % YOUR CODE HERE
  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  for i=1:N
      loglikelihood(iter) = loglikelihood(iter) + logsumexp(ClassProb(i,:));
      ClassProb(i, :) =  exp(ClassProb(i, :) - logsumexp(ClassProb(i,:)));
  end
  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  
  % Print out loglikelihood
  disp(sprintf('EM iteration %d: log likelihood: %f', ...
    iter, loglikelihood(iter)));
  if exist('OCTAVE_VERSION')
    fflush(stdout);
  end
  
  % Check for overfitting: when loglikelihood decreases
  if iter > 1
    if loglikelihood(iter) < loglikelihood(iter-1)
      break;
    end
  end
  
end

% Remove iterations if we exited early
loglikelihood = loglikelihood(1:iter);
