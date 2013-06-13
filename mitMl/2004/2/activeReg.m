%6.867 Problem Set 2, Fall 2004

clear all;
num_trials = 30;
for c_trial=1:num_trials
%load housing data matrix
data=load('mpg.dat');

x=data(:,3:4); %vehicle features
y=data(:,8); %MPG

var_ratio=0;

num_start=size(x,2)+1; %start with at least one training point per parameter
test_start=150; %all examples after this index are test examples
num_active=test_start-num_start;

rand_index=randperm(test_start);
train_index=rand_index(1:num_start);

[trainE,testE,w] = trainNtest(x(train_index,:),y(train_index),...
                              x((test_start+1):end,:),y((test_start+1): ...
                                                  end),var_ratio);
res=[trainE,testE,num_start];

X=[ones(length(train_index),1) x(train_index,:)];
w_cov=pinv(X'*X);

train_index_act=train_index;
train_index_pas=train_index;

%add one actively selected example at a time, in a loop
for c_active=1:num_active
  %pick next example to add to training set
  X_candidate=[ones(size(x,1),1) x(:,:)];
  output_variance=diag(X_candidate*w_cov*(X_candidate'));
  [y_sort,i_sort]=sort(output_variance);
  train_index_act=[train_index_act, i_sort(end)];
  
  %train_index_pas=rand_index(1:(num_start+c_active));
  rand_index=randperm(test_start);
  train_index_pas=[train_index_pas, rand_index(1)];
  %calculate new weight covariance matrix
  X=[ones(length(train_index_act),1) x(train_index_act,:)];
  w_cov=pinv(X'*X);

  %do training for both active and passive learning
  [trainEact,testEact,wact] = trainNtest(x(train_index_act,:),y(train_index_act),...
                                         x((test_start+1):end,:),y((test_start+1): ...
                                                    end),var_ratio);
  [trainEpas,testEpas,wpas] = trainNtest(x(train_index_pas,:),y(train_index_pas),...
                                         x((test_start+1):end,:),y((test_start+1): ...
                                                    end),var_ratio);
  res=[res;testEact,testEpas,c_active+num_start];
end

errors_matrix(:,:,c_trial)=res;
c_trial
%train_index_act
%train_index_pas
end

mean_error=mean(errors_matrix,3);
figure;plot(mean_error(:,3),mean_error(:,1),'r-');
plot(mean_error(2:end,3),mean_error(2:end,1),'r-'); hold on;
plot(mean_error(2:end,3),mean_error(2:end,2),'b-');
xlabel('number of training samples'); ylabel('test error');
legend('active learning','passive learning');
axis([0 180 0 70]);
