load_p1_a;
%[theta k] = perceptron_train(X, y);
%k
%plot_points_and_classifier(X,y,theta);

%angle = sum(theta .* [1 0]') / (normest(theta) * normest([1 0]))

theta = svm_train(X, y);



