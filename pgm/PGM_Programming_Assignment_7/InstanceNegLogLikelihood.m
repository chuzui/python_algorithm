% function [nll, grad] = InstanceNegLogLikelihood(X, y, theta, modelParams)
% returns the negative log-likelihood and its gradient, given a CRF with parameters theta,
% on data (X, y). 
%
% Inputs:
% X            Data.                           (numCharacters x numImageFeatures matrix)
%              X(:,1) is all ones, i.e., it encodes the intercept/bias term.
% y            Data labels.                    (numCharacters x 1 vector)
% theta        CRF weights/parameters.         (numParams x 1 vector)
%              These are shared among the various singleton / pairwise features.
% modelParams  Struct with three fields:
%   .numHiddenStates     in our case, set to 26 (26 possible characters)
%   .numObservedStates   in our case, set to 2  (each pixel is either on or off)
%   .lambda              the regularization parameter lambda
%
% Outputs:
% nll          Negative log-likelihood of the data.    (scalar)
% grad         Gradient of nll with respect to theta   (numParams x 1 vector)
%
% Copyright (C) Daphne Koller, Stanford Univerity, 2012

function [nll, grad] = InstanceNegLogLikelihood(X, y, theta, modelParams)

    % featureSet is a struct with two fields:
    %    .numParams - the number of parameters in the CRF (this is not numImageFeatures
    %                 nor numFeatures, because of parameter sharing)
    %    .features  - an array comprising the features in the CRF.
    %
    % Each feature is a binary indicator variable, represented by a struct 
    % with three fields:
    %    .var          - a vector containing the variables in the scope of this feature
    %    .assignment   - the assignment that this indicator variable corresponds to
    %    .paramIdx     - the index in theta that this feature corresponds to
    %
    % For example, if we have:
    %   
    %   feature = struct('var', [2 3], 'assignment', [5 6], 'paramIdx', 8);
    %
    % then feature is an indicator function over X_2 and X_3, which takes on a value of 1
    % if X_2 = 5 and X_3 = 6 (which would be 'e' and 'f'), and 0 otherwise. 
    % Its contribution to the log-likelihood would be theta(8) if it's 1, and 0 otherwise.
    %
    % If you're interested in the implementation details of CRFs, 
    % feel free to read through GenerateAllFeatures.m and the functions it calls!
    % For the purposes of this assignment, though, you don't
    % have to understand how this code works. (It's complicated.)
    featureSet = GenerateAllFeatures(X, modelParams);
    
    % Use the featureSet to calculate nll and grad.
    % This is the main part of the assignment, and it is very tricky - be careful!
    % You might want to code up your own numerical gradient checker to make sure
    % your answers are correct.
    %
    % Hint: you can use CliqueTreeCalibrate to calculate logZ effectively. 
    %       We have halfway-modified CliqueTreeCalibrate; complete our implementation 
    %       if you want to use it to compute logZ.
    
    nll = 0;
    grad = zeros(size(theta));
    %%%
    % Your code here:
    temp = zeros(size(theta));
    featuresCount = zeros(size(theta));
    [numCharacters numImageFeatures] = size(X);
    chars = modelParams.numHiddenStates;
    single = repmat(struct ('var', [], 'card', [chars], 'val', zeros(1 , chars)), numCharacters, 1);
    double = repmat(struct ('var', [], 'card', [chars chars], 'val', zeros(1, chars * chars)), numCharacters - 1, 1);
    for i=1:numCharacters
        single(i).var = i;
    end
    
    for i=1:(numCharacters-1)
        double(i).var = [i i+1];
    end
    
    for i = 1:length(featureSet.features)
		index = featureSet.features(i).paramIdx;
        f = featureSet.features(i);
        if length(f.var) == 1
            v = GetValueOfAssignment(single(f.var), f.assignment);
            single(f.var) = SetValueOfAssignment(single(f.var), f.assignment, theta(index) + v);
            if y(f.var) == f.assignment
                featuresCount(index) = 1;
            end
            
        else
            v = GetValueOfAssignment(double(f.var(1)), f.assignment);
            double(f.var(1)) = SetValueOfAssignment(double(f.var(1)), f.assignment, theta(index) + v);
            
            if all(y(f.var) == f.assignment)
                featuresCount(index) = 1;
            end
           
        end
    end
%     for i = 1:length(featureSet.features)
% 		index = featureSet.features(i).paramIdx;
% 		if length(factors(index).var) ~= 0
% 			v = GetValueOfAssignment(factors(index), featureSet.features(i).assignment) + theta(index);
% 			factors(index) = SetValueOfAssignment(factors(index), featureSet.features(i).assignment, v);
% 		else
% 			factors(index).var = featureSet.features(i).var;
% 			if length(factors(index).var) == 1
% 				factors(index).card = [numCharacters];	
% 			elseif length(factors(index).var) == 2
% 				if any(featureSet.features(i).assignment > 26)
% 					display "> 26"
% 				end
% 				factors(index).card = [numCharacters numCharacters];
% 			else		
% 				factors(index).card = [numImageFeatures numCharacters 2];
% 			end	
% 			factors(index).val = zeros(1, prod(factors(index).card));
% 			factors(index) = SetValueOfAssignment(factors(index), featureSet.features(i).assignment, theta(index));
% 
% 		end
%     end
    %for i = 1:length(factors)
		%factors(i).val = exp(factors(i).val);
    %end
    factors = [single(:); double(:)];
    for i = 1:length(factors)
        factors(i).val = exp(factors(i).val);
    end
    P = CreateCliqueTree(factors);
    [a logZ] = CliqueTreeCalibrate(P, false);
    
    weighted = sum(theta .* featuresCount);
    reg = (modelParams.lambda / 2) * sum(theta .^ 2)
    
    nll = logZ - weighted + reg;
    
    a.cliqueList(1).val = a.cliqueList(1).val / sum(a.cliqueList(1).val);
    a.cliqueList(2).val = a.cliqueList(2).val / sum(a.cliqueList(2).val);
    single(1) =  FactorMarginalization(a.cliqueList(1), [2]);
    single(2) =  FactorMarginalization(a.cliqueList(1), [1]);
    single(3) =  FactorMarginalization(a.cliqueList(2), [2]);
    
    double(1) = a.cliqueList(1);
    double(2) = a.cliqueList(2);
    
    for i=1:numCharacters
        single(i).val = single(i).val / sum(single(i).val);
        %single(i).val = log(single(i).val );
    end
    
    for i=1:(numCharacters-1)
        double(i).val = double(i).val / sum(double(i).val);
        %double(i).val = log(double(i).val);
    end
    
    for i = 1:length(featureSet.features)
		index = featureSet.features(i).paramIdx;
        f = featureSet.features(i);
        if length(f.var) == 1
            v = GetValueOfAssignment(single(f.var), f.assignment);
            temp(index) = temp(index) +  v;
        else
            v = GetValueOfAssignment(double(f.var(1)), f.assignment);
            temp(index) = temp(index) + v;
        end
    end
    
    grad = temp - featuresCount + modelParams.lambda * theta;
    
    %index = 1;
    %for i = 1:modelParams.numHiddenStates
		%factors(i).var = featureSet.features(i).var;
		%factors(i).card = [modelParams.numHiddenStates];
		%factors(i).val = zeros(1, modelParams.numHiddenStates);
		%v = sum(index, i+numCharacters-1);
		%factors(i) = SetValueOfAssignment(factors(i), featureSet.features(i).assignment, v);
		%index = index + numCharacters	;
    %end
    

end
