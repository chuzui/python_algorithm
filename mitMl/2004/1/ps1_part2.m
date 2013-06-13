%6.867 Problem Set 1, Fall 2004

%load housing data matrix
data=load('housing.data');

x=data(:,13); %LSTAT
y=data(:,14); %house-price

numtrain=250; %number of training examples

var_ratio=0; %ratio of \sigma^2 to \alpha^2
var_ratio = 1;
Results = [];
for deg=1:7, %order of polynomial model
   %call training and testing routines for polynomial model
   [trainE,testE]=testPoly(x,y,numtrain,deg,var_ratio);
   Results = [Results; deg, trainE, testE];
end;

plot(Results(:,1),Results(:,2:3));
xlabel('polynomial order');
legend('training error', 'test error');
grid on;

