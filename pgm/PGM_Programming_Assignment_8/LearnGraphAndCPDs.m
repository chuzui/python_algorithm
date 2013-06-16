function [P G loglikelihood] = LearnGraphAndCPDs(dataset, labels)

% dataset: N x 10 x 3, N poses represented by 10 parts in (y, x, alpha) 
% labels: N x 2 true class labels for the examples. labels(i,j)=1 if the 
%         the ith example belongs to class j
%
% Copyright (C) Daphne Koller, Stanford Univerity, 2012

N = size(dataset, 1);
K = size(labels,2);

G = zeros(10,2,K); % graph structures to learn
% initialization
for k=1:K
    G(2:end,:,k) = ones(9,2);
end

% estimate graph structure for each class
for k=1:K
    % fill in G(:,:,k)
    % use ConvertAtoG to convert a maximum spanning tree to a graph G
    %%%%%%%%%%%%%%%%%%%%%%%%%
    % YOUR CODE HERE
    %%%%%%%%%%%%%%%%%%%%%%%%%
    [A W] = LearnGraphStructure(dataset(find(labels(:, k)), :, :));
    G(:, :, k) = ConvertAtoG(A);
end

% estimate parameters

P.c = zeros(1,K);
% compute P.c

% the following code can be copied from LearnCPDsGivenGraph.m
% with little or no modification
%%%%%%%%%%%%%%%%%%%%%%%%%
% YOUR CODE HERE
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

for i=1:K
    P.c(i) = sum(labels(:, i)) / N;
end

P.clg = repmat(struct('mu_y', [], 'sigma_y', [], 'mu_x', [], 'sigma_x', [], 'mu_angle', [], 'sigma_angle', [], 'theta', []), 1, 10);
for i = 1:10
    for k=1:K 
        if G(i, 1, k) == 0
            [P.clg(i).mu_y(k) P.clg(i).sigma_y(k)] = FitGaussianParameters(reshape(dataset(find(labels(:, k)), i, 1), sum(labels(:, k)), 1)); 
            [P.clg(i).mu_x(k) P.clg(i).sigma_x(k)] = FitGaussianParameters(reshape(dataset(find(labels(:, k)), i, 2), sum(labels(:, k)), 1)); 
            [P.clg(i).mu_angle(k) P.clg(i).sigma_angle(k)] = FitGaussianParameters(reshape(dataset(find(labels(:, k)), i, 3), sum(labels(:, k)), 1)); 
        else
            pa = G(i, 2, k);
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
        end
    end

   
end

loglikelihood = ComputeLogLikelihood(P, G, dataset);

fprintf('log likelihood: %f\n', loglikelihood);