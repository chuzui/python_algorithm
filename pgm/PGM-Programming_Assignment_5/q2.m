addpath '4'

[toy_network, toy_factors] = ConstructToyNetwork(.5, .5);

P = CreateClusterGraph(toy_factors, []);
    [P MESSAGES] = ClusterGraphCalibrate(P, 0);

M = ComputeExactMarginalsBP(toy_factors, [], 0);
