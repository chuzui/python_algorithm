% Copyright (C) Daphne Koller, Stanford University, 2012

function [MEU OptimalDecisionRule] = OptimizeMEU( I )

  % Inputs: An influence diagram I with a single decision node and a single utility node.
  %         I.RandomFactors = list of factors for each random variable.  These are CPDs, with
  %              the child variable = D.var(1)
  %         I.DecisionFactors = factor for the decision node.
  %         I.UtilityFactors = list of factors representing conditional utilities.
  % Return value: the maximum expected utility of I and an optimal decision rule 
  % (represented again as a factor) that yields that expected utility.
  
  % We assume I has a single decision node.
  % You may assume that there is a unique optimal decision.
  D = I.DecisionFactors(1);

  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  %
  % YOUR CODE HERE...
  % 
  % Some other information that might be useful for some implementations
  % (note that there are multiple ways to implement this):
  % 1.  It is probably easiest to think of two cases - D has parents and D 
  %     has no parents.
  % 2.  You may find the Matlab/Octave function setdiff useful.
  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%    
  f = CalculateExpectedUtilityFactor(I);
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
