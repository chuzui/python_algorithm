function [clusters, centroids] = k_means(X, k)

m = size(X, 1);
n = size(X, 2);
oldCentroids = zeros(k, n);
centroids = X(ceil(rand(k, 1)*m), :);

while (norm(oldCentroids - centroids) > 1e-15)
	oldCentroids = centroids;
	
	for i=1:m
		dists = sum((repmat(X(i, :), k, 1) - centroids) .^ 2, 2);
		[min_dist clusters(i, 1)] = min(dists);
	end

	draw_clusters(X, clusters, centroids);
	pause(1);
	
	for i=1:k
		centroids(i,:) = mean(X(clusters == i, :));
	end
end
%%% YOUR CODE HERE
