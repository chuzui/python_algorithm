function loglikelihood = ComputeLogLikelihood(P, G, dataset)
% returns the (natural) log-likelihood of data given the model and graph structure
%
% Inputs:
% P: struct array parameters (explained in PA description)
% G: graph structure and parameterization (explained in PA description)
%
%    NOTICE that G could be either 10x2 (same graph shared by all classes)
%    or 10x2x2 (each class has its own graph). your code should compute
%    the log-likelihood using the right graph.
%
% dataset: N x 10 x 3, N poses represented by 10 parts in (y, x, alpha)
% 
% Output:
% loglikelihood: log-likelihood of the data (scalar)
%
% Copyright (C) Daphne Koller, Stanford Univerity, 2012
if size(G, 3) == 1
    G = repmat(G, [1, 1, 2]);
end

N = size(dataset,1); % number of examples
K = length(P.c); % number of classes

loglikelihood = 0;
% You should compute the log likelihood of data as in eq. (12) and (13)
% in the PA description
% Hint: Use lognormpdf instead of log(normpdf) to prevent underflow.
%       You may use log(sum(exp(logProb))) to do addition in the original
%       space, sum(Prob).
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% YOUR CODE HERE
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
for i=1:N
    oneP = 0;
    for c=1:K
        g = G(:,:, c);
        log_sum = 0;
        for k=1:size(g, 1)
            if g(k,1) == 0
                log_sum = log_sum + lognormpdf(dataset(i, k, 1), P.clg(k).mu_y(c), P.clg(k).sigma_y(c)) ...,
                + lognormpdf(dataset(i, k, 2), P.clg(k).mu_x(c), P.clg(k).sigma_x(c)) ..., 
                + lognormpdf(dataset(i, k, 3), P.clg(k).mu_angle(c), P.clg(k).sigma_angle(c));            
            else
                pa = g(k, 2);
                theta = P.clg(k).theta;
                log_sum = log_sum + lognormpdf(dataset(i, k, 1), sum(theta(c, 1:4) .* [1, reshape(dataset(i, pa, :),1,3)]), P.clg(k).sigma_y(c)) ...,
                + lognormpdf(dataset(i, k, 2),sum(theta(c, 5:8) .* [1, reshape(dataset(i, pa, :),1,3)]), P.clg(k).sigma_x(c)) ..., 
                + lognormpdf(dataset(i, k, 3), sum(theta(c, 9:12) .* [1, reshape(dataset(i, pa, :),1,3)]), P.clg(k).sigma_angle(c));
            end
        end
        oneP = oneP + P.c(c) * exp(log_sum);
    end
    loglikelihood = loglikelihood + log(oneP);
end
loglikelihood
