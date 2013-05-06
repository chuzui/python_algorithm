%CLIQUETREECALIBRATE Performs sum-product or max-product algorithm for 
%clique tree calibration.

%   P = CLIQUETREECALIBRATE(P, isMax) calibrates a given clique tree, P 
%   according to the value of isMax flag. If isMax is 1, it uses max-sum
%   message passing, otherwise uses sum-product. This function 
%   returns the clique tree where the .val for each clique in .cliqueList
%   is set to the final calibrated potentials.
%
% Copyright (C) Daphne Koller, Stanford University, 2012

function P = CliqueTreeCalibrate(P, isMax)


% Number of cliques in the tree.
N = length(P.cliqueList);

% Setting up the messages that will be passed.
% MESSAGES(i,j) represents the message going from clique i to clique j. 
MESSAGES = repmat(struct('var', [], 'card', [], 'val', []), N, N);

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%
% We have split the coding part for this function in two chunks with
% specific comments. This will make implementation much easier.
%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%
% YOUR CODE HERE
% While there are ready cliques to pass messages between, keep passing
% messages. Use GetNextCliques to find cliques to pass messages between.
% Once you have clique i that is ready to send message to clique
% j, compute the message and put it in MESSAGES(i,j).
% Remember that you only need an upward pass and a downward pass.
%
 %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
 if isMax == 1
     factor_prod = @(x,y)FactorSum(x,y);
     marginal = @(x,y)FactorMaxMarginalization(x,y);
 else
     factor_prod = @(x,y)FactorProduct(x,y);
     marginal = @(x,y)FactorMarginalization(x,y);
 end
[i, j] = GetNextCliques(P, MESSAGES);
while all([i, j])
    F = P.cliqueList(i);
    for k = 1:N
        if P.edges(k, i) == 1 && k ~= j
            F = factor_prod(F, MESSAGES(k, i));
        end
    end
    V = intersect(P.cliqueList(i).var,P.cliqueList(j).var);
    F = marginal(F,setdiff(F.var, V));
    if isMax == 0
        F.val = F.val ./ sum(F.val);
    end
    MESSAGES(i, j) = F;
    [i, j] = GetNextCliques(P, MESSAGES);
end

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% YOUR CODE HERE
%
% Now the clique tree has been calibrated. 
% Compute the final potentials for the cliques and place them in P.
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
for k = 1:N
    F = P.cliqueList(k);
    for m = 1:N
        if P.edges(m, k) == 1
            F = factor_prod(F, MESSAGES(m, k));
        end
    end
    P.cliqueList(k) = F;
end

return
