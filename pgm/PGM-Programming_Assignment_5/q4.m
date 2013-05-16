[toy_network, toy_factors] = ConstructToyNetwork(1.0, 0.1);
A0 = i * ones(1, length(toy_network.names));
[M, all_samples] = ...
            MCMCInference(toy_network, toy_factors, [], 'Gibbs', 0, 4000, 1, A0);