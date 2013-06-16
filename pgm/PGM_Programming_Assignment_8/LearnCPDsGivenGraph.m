function [P loglikelihood] = LearnCPDsGivenGraph(dataset, G, labels)
%
% Inputs:
% dataset: N x 10 x 3, N poses represented by 10 parts in (y, x, alpha)
% G: graph parameterization as explained in PA description
% labels: N x 2 true class labels for the examples. labels(i,j)=1 if the 
%         the ith example belongs to class j and 0 elsewhere        
%
% Outputs:
% P: struct array parameters (explained in PA description)
% loglikelihood: log-likelihood of the data (scalar)
%
% Copyright (C) Daphne Koller, Stanford Univerity, 2012

N = size(dataset, 1);
K = size(labels,2);

loglikelihood = 0;
P.c = zeros(1,K);

% estimate parameters
% fill in P.c, MLE for class probabilities
% fill in P.clg for each body part and each class
% choose the right parameterization based on G(i,1)
% compute the likelihood - you may want to use ComputeLogLikelihood.m
% you just implemented.
%%%%%%%%%%%%%%%%%%%%%%%%%
% YOUR CODE HERE
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
fprintf('log likelihood: %f\n', loglikelihood);
for i=1:K
    P.c(i) = sum(labels(:, i)) / N;
end

P.clg = repmat(struct('mu_y', [], 'sigma_y', [], 'mu_x', [], 'sigma_x', [], 'mu_angle', [], 'sigma_angle', [], 'theta', []), 1, 10);
for i = 1:10
    if G(i, 1) == 0
        for k=1:K       
            [P.clg(i).mu_y(k) P.clg(i).sigma_y(k)] = FitGaussianParameters(reshape(dataset(find(labels(:, k)), i, 1), sum(labels(:, k)), 1)); 
            [P.clg(i).mu_x(k) P.clg(i).sigma_x(k)] = FitGaussianParameters(reshape(dataset(find(labels(:, k)), i, 2), sum(labels(:, k)), 1)); 
            [P.clg(i).mu_angle(k) P.clg(i).sigma_angle(k)] = FitGaussianParameters(reshape(dataset(find(labels(:, k)), i, 3), sum(labels(:, k)), 1)); 
        end
    else
        for k=1:K
            pa = G(i, 2);
            num = sum(labels(:, k));
            U = reshape(dataset(find(labels(:, k)), pa, :), sum(labels(:, k)), 3);
            %Ux = reshape(dataset(find(labels(:, k)), pa, 2), sum(labels(:, k)), 1);
            %Uangle = reshape(dataset(find(labels(:, k)), pa, 3), sum(labels(:, k)), 1);
            
            y = dataset(find(labels(:, k)), i, 1);
            [Beta P.clg(i).sigma_y(k)] = FitLinearGaussianParameters(y, U);
            P.clg(i).theta(k, 1:4) = [Beta(4), Beta(1:3)']; 
            
            x = dataset(find(labels(:, k)), i, 2);
            [Beta P.clg(i).sigma_x(k)] = FitLinearGaussianParameters(x, U);
            P.clg(i).theta(k, 5:8) = [Beta(4), Beta(1:3)']; 
            
            angle = dataset(find(labels(:, k)), i, 3);
            [Beta P.clg(i).sigma_angle(k)] = FitLinearGaussianParameters(angle, U);
            P.clg(i).theta(k, 9:12) = [Beta(4), Beta(1:3)']; 
            %[P.clg(i).mu_y(k) P.clg(i).sigma_y(k)] = FitGaussianParameters(reshape(dataset(find(labels(:, k)), i, 1), sum(labels(:, k)), 1)); 
        end
    end
end

loglikelihood = ComputeLogLikelihood(P, G, dataset);

