% Copyright (C) Daphne Koller, Stanford University, 2012

function EUF = CalculateExpectedUtilityFactor( I )

  % Inputs: An influence diagram I with a single decision node and a single utility node.
  %         I.RandomFactors = list of factors for each random variable.  These are CPDs, with
  %              the child variable = D.var(1)
  %         I.DecisionFactors = factor for the decision node.
  %         I.UtilityFactors = list of factors representing conditional utilities.
  % Return value: A factor over the scope of the decision rule D from I that
  % gives the conditional utility given each assignment for D.var
  %
  % Note - We assume I has a single decision node and utility node.
  EUF = [];
  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  %
  % YOUR CODE HERE...
  %
  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%  
  %I.DecisionFactors(1).val(:) = 1;
  F = [I.RandomFactors];
  U = I.UtilityFactors(1);
  F = [F, U];
  V = unique([F(:).var]);
  %newF = struct('var', [], 'card', [], 'val', []);
  newF = VariableElimination(F, setdiff(V,I.DecisionFactors(1).var));
 % for f = F
 %     newF = FactorProduct(newF, f);
 % end
 % newF = FactorProduct(newF, U);
 f = newF(1);
 for i = 2:length(newF);
     f = FactorProduct(f, newF(i));
 end
  %newF = FactorMarginalization(newF, setdiff(newF.var, I.DecisionFactors(1).var));
  EUF = f;
end  
