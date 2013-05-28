% Copyright (C) Daphne Koller, Stanford University, 2012

function [MEU OptimalDecisionRule] = OptimizeLinearExpectations( I )
  % Inputs: An influence diagram I with a single decision node and one or more utility nodes.
  %         I.RandomFactors = list of factors for each random variable.  These are CPDs, with
  %              the child variable = D.var(1)
  %         I.DecisionFactors = factor for the decision node.
  %         I.UtilityFactors = list of factors representing conditional utilities.
  % Return value: the maximum expected utility of I and an optimal decision rule 
  % (represented again as a factor) that yields that expected utility.
  % You may assume that there is a unique optimal decision.
  %
  % This is similar to OptimizeMEU except that we will have to account for
  % multiple utility factors.  We will do this by calculating the expected
  % utility factors and combining them, then optimizing with respect to that
  % combined expected utility factor.  
  MEU = [];
  OptimalDecisionRule = [];
  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  %
  % YOUR CODE HERE
  %
  % A decision rule for D assigns, for each joint assignment to D's parents, 
  % probability 1 to the best option from the EUF for that joint assignment 
  % to D's parents, and 0 otherwise.  Note that when D has no parents, it is
  % a degenerate case we can handle separately for convenience.
  %
  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  D = I.DecisionFactors(1);
  temp = I;
  temp.UtilityFactors = I.UtilityFactors(1);
  f = CalculateExpectedUtilityFactor(temp);
  for i = 2:length(I.UtilityFactors)
      temp.UtilityFactors = I.UtilityFactors(i);
      temp_factor = CalculateExpectedUtilityFactor(temp);
      f.val = f.val + temp_factor.val;
  end
  if length(D.var) == 1
      [maxValue index] = max(f.val);
      MEU = maxValue;
      f.val(:) = 0;
      f.val(index) = 1;
      OptimalDecisionRule = f;
  else
      d_factor =  FactorMarginalization(f, setdiff(f.var, D.var(1)));
     
      OptimalDecisionRule = f;
      OptimalDecisionRule.val(:) = 0;
      
      ass = IndexToAssignment(1:prod(D.card), D.card);
      pa = unique(ass(:, 2:end), 'rows');
      for i = pa'     
          templeAss = ass(find(all(ass(:, 2:end) == repmat(i', size(ass, 1), 1), 2)), :);
          [maxValue index] = max(GetValueOfAssignment(f, templeAss));
          OptimalDecisionRule = SetValueOfAssignment(OptimalDecisionRule, templeAss(index, :), 1);
      end
      
      MEU = sum(OptimalDecisionRule.val .* f.val); 
  end



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
if all(A.val >= 0)
    A.val = log(A.val);  
end

if all(B.val >= 0)
   B.val = log(B.val);   
end

C.val = A.val(indxA) + B.val(indxB);
 

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

end
