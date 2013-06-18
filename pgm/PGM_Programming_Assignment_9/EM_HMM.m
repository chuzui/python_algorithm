% File: EM_HMM.m
%
% Copyright (C) Daphne Koller, Stanford Univerity, 2012

function [P loglikelihood ClassProb PairProb] = EM_HMM(actionData, poseData, G, InitialClassProb, InitialPairProb, maxIter)

% INPUTS
% actionData: structure holding the actions as described in the PA
% poseData: N x 10 x 3 matrix, where N is number of poses in all actions
% G: graph parameterization as explained in PA description
% InitialClassProb: N x K matrix, initial allocation of the N poses to the K
%   states. InitialClassProb(i,j) is the probability that example i belongs
%   to state j.
%   This is described in more detail in the PA.
% InitialPairProb: V x K^2 matrix, where V is the total number of pose
%   transitions in all HMM action models, and K is the number of states.
%   This is described in more detail in the PA.
% maxIter: max number of iterations to run EM

% OUTPUTS
% P: structure holding the learned parameters as described in the PA
% loglikelihood: #(iterations run) x 1 vector of loglikelihoods stored for
%   each iteration
% ClassProb: N x K matrix of the conditional class probability of the N examples to the
%   K states in the final iteration. ClassProb(i,j) is the probability that
%   example i belongs to state j. This is described in more detail in the PA.
% PairProb: V x K^2 matrix, where V is the total number of pose transitions
%   in all HMM action models, and K is the number of states. This is
%   described in more detail in the PA.

% Initialize variables
N = size(poseData, 1);
K = size(InitialClassProb, 2);
L = size(actionData, 2); % number of actions
V = size(InitialPairProb, 1);

ClassProb = InitialClassProb;
PairProb = InitialPairProb;

loglikelihood = zeros(maxIter,1);   

P.c = [];
P.clg.sigma_x = [];
P.clg.sigma_y = [];
P.clg.sigma_angle = [];
P.clg = repmat(struct('mu_y', [], 'sigma_y', [], 'mu_x', [], 'sigma_x', [], 'mu_angle', [], 'sigma_angle', [], 'theta', []), 1, 10);
% EM algorithm
for iter=1:maxIter
  
  % M-STEP to estimate parameters for Gaussians
  % Fill in P.c, the initial state prior probability (NOT the class probability as in PA8 and EM_cluster.m)
  % Fill in P.clg for each body part and each class
  % Make sure to choose the right parameterization based on G(i,1)
  % Hint: This part should be similar to your work from PA8 and EM_cluster.m
  
  P.c = zeros(1,K);
  
  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  % YOUR CODE HERE
  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  s = zeros(1, K);
  for i=1:L
     s = s + ClassProb(actionData(i).marg_ind(1), :);   
  end
   P.c =s/ sum(sum(s));


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
  
  % M-STEP to estimate parameters for transition matrix
  % Fill in P.transMatrix, the transition matrix for states
  % P.transMatrix(i,j) is the probability of transitioning from state i to state j
  P.transMatrix = zeros(K,K);
  
  % Add Dirichlet prior based on size of poseData to avoid 0 probabilities
  P.transMatrix = P.transMatrix + size(PairProb,1) * .05;
  
  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  % YOUR CODE HERE
  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  P.transMatrix = P.transMatrix + reshape(sum(PairProb), K, K);
  for i=1:K
      P.transMatrix(i,:) = exp(log((P.transMatrix(i,:))) - log(sum(P.transMatrix(i,:))));
  end
  
  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  
    
  % E-STEP preparation: compute the emission model factors (emission probabilities) in log space for each 
  % of the poses in all actions = log( P(Pose | State) )
  % Hint: This part should be similar to (but NOT the same as) your code in EM_cluster.m
  
      logEmissionProb = zeros(N,K);
  
  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  % YOUR CODE HERE
  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
   for i=1:N
    for c=1:K
        g = G(:,:);
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
        logEmissionProb(i,c) = log_sum;
    end
    %ClassProb(i, :) =  exp(ClassProb(i, :) - logsumexp(ClassProb(i,:)));
    end
  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  
    
  % E-STEP to compute expected sufficient statistics
  % ClassProb contains the conditional class probabilities for each pose in all actions
  % PairProb contains the expected sufficient statistics for the transition CPDs (pairwise transition probabilities)
  % Also compute log likelihood of dataset for this iteration
  % You should do inference and compute everything in log space, only converting to probability space at the end
  % Hint: You should use the logsumexp() function here to do probability normalization in log space to avoid numerical issues
  
  ClassProb = zeros(N,K);
  PairProb = zeros(V,K^2);
  loglikelihood(iter) = 0;
  
  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  % YOUR CODE HERE
  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  for i=1:L
      lf = [];
      init_f = struct('var', [1], 'card', [K], 'val', []);
      init_f.val = log(P.c);
      lf = [lf, init_f];
      for j=1:length(actionData(i).marg_ind)
          f = struct('var', [j], 'card', [K], 'val', []);
          f.val = logEmissionProb(actionData(i).marg_ind(j),:);
          lf = [lf, f];
      end
      for j=1:length(actionData(i).pair_ind)
          f = struct('var', [j, j+1], 'card', [K, K], 'val', []);
          f.val = log(P.transMatrix(:)');
          lf = [lf, f];
      end
      [M PCalibrated] = ComputeExactMarginalsHMM(lf);
      for j=1:length(actionData(i).marg_ind)
          l = M(j).val;
          ClassProb(actionData(i).marg_ind(j), :) = exp(l- logsumexp(l));
      end
     
      for j=1:length(actionData(i).pair_ind)
          l = PCalibrated.cliqueList(j).val;
          PairProb(actionData(i).pair_ind(j), :) = exp(l- logsumexp(l));
      end
      
       l = PCalibrated.cliqueList(1).val;
       loglikelihood(iter) = loglikelihood(iter)+ logsumexp(l);
  end
  
  %for i=1:N
   %   loglikelihood(iter) = loglikelihood(iter) + logsumexp(logEmissionProb(i,:));
  %end
  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  
  % Print out loglikelihood
  disp(sprintf('EM iteration %d: log likelihood: %f', ...
    iter, loglikelihood(iter)));
  if exist('OCTAVE_VERSION')
    fflush(stdout);
  end
  
  % Check for overfitting by decreasing loglikelihood
  if iter > 1
    if loglikelihood(iter) < loglikelihood(iter-1)
      break;
    end
  end
  
end

% Remove iterations if we exited early
loglikelihood = loglikelihood(1:iter);
