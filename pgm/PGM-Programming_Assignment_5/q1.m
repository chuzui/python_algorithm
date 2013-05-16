    [toy_network, toy_factors] = ConstructRandNetwork(0.3, 0.7);
    P = CreateClusterGraph(toy_factors, []);
    [P MESSAGES] = ClusterGraphCalibrate(P, 0);