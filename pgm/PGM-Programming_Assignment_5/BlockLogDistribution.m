%BLOCKLOGDISTRIBUTION
%
%   LogBS = BlockLogDistribution(V, G, F, A) returns the log of a
%   block-sampling array (which contains the log-unnormalized-probabilities of
%   selecting each label for the block), given variables V to block-sample in
%   network G with factors F and current assignment A.  Note that the variables
%   in V must all have the same dimensionality.
%
%   Input arguments:
%   V -- an array of variable names
%   G -- the graph with the following fields:
%     .names - a cell array where names{i} = name of variable i in the graph 
%     .card - an array where card(i) is the cardinality of variable i
%     .edges - a matrix such that edges(i,j) shows if variables i and j 
%              have an edge between them (1 if so, 0 otherwise)
%     .var2factors - a cell array where var2factors{i} gives an array where the
%              entries are the indices of the factors including variable i
%   F -- a struct array of factors.  A factor has the following fields:
%       F(i).var - names of the variables in factor i
%       F(i).card - cardinalities of the variables in factor i
%       F(i).val - a vectorized version of the CPD for factor i (raw probability)
%   A -- an array with 1 entry for each variable in G s.t. A(i) is the current
%       assignment to variable i in G.
%
%   Each entry in LogBS is the log-probability that that value is selected.
%   LogBS is the P(V | X_{-v} = A_{-v}, all X_i in V have the same value), where
%   X_{-v} is the set of variables not in V and A_{-v} is the corresponding
%   assignment to these variables consistent with A.  In the case that |V| = 1,
%   this reduces to Gibbs Sampling.  NOTE that exp(LogBS) is not normalized to
%   sum to one at the end of this function (nor do you need to worry about that
%   in this function).
%
% Copyright (C) Daphne Koller, Stanford University, 2012

function LogBS = BlockLogDistribution(V, G, F, A)
if length(unique(G.card(V))) ~= 1
    disp('WARNING: trying to block sample invalid variable set');
    return;
end

% d is the dimensionality of all the variables we are extracting
d = G.card(V(1));

LogBS = zeros(1, d);
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% YOUR CODE HERE
% Compute LogBS by multiplying (adding in log-space) in the correct values from
% each factor that includes some variable in V.  
%
% NOTE: As this is called in the innermost loop of both Gibbs and Metropolis-
% Hastings, you should make this fast.  You may want to make use of
% G.var2factors, repmat,unique, and GetValueOfAssignment.
%
% Also you should have only ONE for-loop, as for-loops are VERY slow in matlab
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
f = struct('var', [], 'card', [], 'val', []);
E = [];
for i = 1:length(A)
    E = [E; i, A(i)];
end
for i = cell2mat(G.var2factors(V(1)))
    temp_factor = F(i);
    temp_factor.val = log(temp_factor.val);
    f = FactorSum(f, temp_factor);
end
f.val = f.val - min(f.val);
f = ObserveEvidence(f,E);
f = FactorMarginalization(f, setdiff(f.var, V));
%f = ObserveEvidence(f, E);
LogBS = f.val;
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% Re-normalize to prevent underflow when you move back to probability space
%LogBS = LogBS - min(LogBS);
end


function C = FactorSum(A, B)

% Check for empty factors
if (isempty(A.var)), C = B; return; end;
if (isempty(B.var)), C = A; return; end;

% Check that variables in both A and B have the same cardinality
[dummy iA iB] = intersect(A.var, B.var);
if ~isempty(dummy)
	% A and B have at least 1 variable in common
	assert(all(A.card(iA) == B.card(iB)), 'Dimensionality mismatch in factors');
end

% Set the variables of C
C.var = union(A.var, B.var);

% Construct the mapping between variables in A and B and variables in C.
% In the code below, we have that
%
%   mapA(i) = j, if and only if, A.var(i) == C.var(j)
% 
% and similarly 
%
%   mapB(i) = j, if and only if, B.var(i) == C.var(j)
%
% For example, if A.var = [3 1 4], B.var = [4 5], and C.var = [1 3 4 5],
% then, mapA = [2 1 3] and mapB = [3 4]; mapA(1) = 2 because A.var(1) = 3
% and C.var(2) = 3, so A.var(1) == C.var(2).

[dummy, mapA] = ismember(A.var, C.var);
[dummy, mapB] = ismember(B.var, C.var);

% Set the cardinality of variables in C
C.card = zeros(1, length(C.var));
C.card(mapA) = A.card;
C.card(mapB) = B.card;

% Initialize the factor values of C:
%   prod(C.card) is the number of entries in C
C.val = log(zeros(1,prod(C.card)));

% Compute some helper indices
% These will be very useful for calculating C.val
% so make sure you understand what these lines are doing.
assignments = IndexToAssignment(1:prod(C.card), C.card);
indxA = AssignmentToIndex(assignments(:, mapA), A.card);
indxB = AssignmentToIndex(assignments(:, mapB), B.card);

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% YOUR CODE HERE:
% Correctly populate the factor values of C
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

C.val = A.val(indxA) + B.val(indxB);
 

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

end

function B = FactorMarginalization(A, V)

% Check for empty factor or variable list
if (isempty(A.var) || isempty(V)), B = A; return; end;

% Construct the output factor over A.var \ V (the variables in A.var that are not in V)
% and mapping between variables in A and B
[B.var, mapB] = setdiff(A.var, V);

% Check for empty resultant factor
if isempty(B.var)
  %error('Error: Resultant factor has empty scope');
  B.var = [];
  B.card = [];
  B.val = [];
  return;
end;

% Initialize B.card and B.val
B.card = A.card(mapB);
B.val = zeros(1,prod(B.card));

% Compute some helper indices
% These will be very useful for calculating C.val
% so make sure you understand what these lines are doing
assignments = IndexToAssignment(1:length(A.val), A.card);
indxB = AssignmentToIndex(assignments(:, mapB), B.card);

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% YOUR CODE HERE
% Correctly populate the factor values of B
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    for i = 1:length(A.val),
        B.val(indxB(i)) = B.val(indxB(i)) + A.val(i);
    end;
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
end

