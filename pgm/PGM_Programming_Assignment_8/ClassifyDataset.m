function accuracy = ClassifyDataset(dataset, labels, P, G)
% returns the accuracy of the model P and graph G on the dataset 
%
% Inputs:
% dataset: N x 10 x 3, N test instances represented by 10 parts
% labels:  N x 2 true class labels for the instances.
%          labels(i,j)=1 if the ith instance belongs to class j 
% P: struct array model parameters (explained in PA description)
% G: graph structure and parameterization (explained in PA description) 
%
% Outputs:
% accuracy: fraction of correctly classified instances (scalar)
%
% Copyright (C) Daphne Koller, Stanford Univerity, 2012

N = size(dataset, 1);
accuracy = 0.0;

if size(G, 3) == 1
    G = repmat(G, [1, 1, 2]);
end

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% YOUR CODE HERE
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

K = length(P.c);
correct = 0;
for i=1:N
    max_value = -inf;
    max_index = 0;
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
        if log_sum > max_value
            max_value = log_sum;
            max_index = c;
        end
    end
    if labels(i, max_index) == 1
        correct = correct + 1;
    end
end
accuracy = correct / N;
fprintf('Accuracy: %.2f\n', accuracy);