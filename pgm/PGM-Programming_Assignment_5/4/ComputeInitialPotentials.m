%COMPUTEINITIALPOTENTIALS Sets up the cliques in the clique tree that is
%passed in as a parameter.
%
%   P = COMPUTEINITIALPOTENTIALS(C) Takes the clique tree skeleton C which is a
%   struct with three fields:
%   - nodes: cell array representing the cliques in the tree.
%   - edges: represents the adjacency matrix of the tree.
%   - factorList: represents the list of factors that were used to build
%   the tree. 
%   
%   It returns the standard form of a clique tree P that we will use through 
%   the rest of the assigment. P is struct with two fields:
%   - cliqueList: represents an array of cliques with appropriate factors 
%   from factorList assigned to each clique. Where the .val of each clique
%   is initialized to the initial potential of that clique.
%   - edges: represents the adjacency matrix of the tree. 
%
% Copyright (C) Daphne Koller, Stanford University, 2012


function P = ComputeInitialPotentials(C)

% number of cliques
N = length(C.nodes);

% initialize cluster potentials 
P.cliqueList = repmat(struct('var', [], 'card', [], 'val', []), N, 1);
P.edges = zeros(N);

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% YOUR CODE HERE
%
% First, compute an assignment of factors from factorList to cliques. 
% Then use that assignment to initialize the cliques in cliqueList to 
% their initial potentials. 

% C.nodes is a list of cliques.
% So in your code, you should start with: P.cliqueList(i).var = C.nodes{i};
% Print out C to get a better understanding of its structure.
%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
M = length(C.factorList);

V = unique([C.factorList(:).var]);
card = zeros(1, length(V));
for i = 1 : length(V),
	 for j = 1 : length(C.factorList)
		  if (~isempty(find(C.factorList(j).var == i)))
				card(i) = C.factorList(j).card(find(C.factorList(j).var == i));
				break;
		  end
	 end
end

for i = 1:N
    P.cliqueList(i).var = C.nodes{i};
    P.cliqueList(i).card = card(P.cliqueList(i).var);
    P.cliqueList(i).val = ones(1, prod(P.cliqueList(i).card));
end
for i = 1:N
    F = struct('var', [], 'card', [], 'val', []);
    j = 1;
    while j <= length(C.factorList)
        if all(ismember(C.factorList(j).var, P.cliqueList(i).var))
            F = FactorProduct(F, C.factorList(j));
            C.factorList(j) = [];
            j = j-1;
        end
        j = j+1;
    end
    P.cliqueList(i) = FactorProduct(P.cliqueList(i), F);
    %P.cliqueList(i) = StandardizeFactors(F);
end
P.edges = C.edges;

end

