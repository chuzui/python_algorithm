%%%%%%% hw1q2d %%%%%%%%
load('q2x.dat');
load('q2y.dat');
x = [ones(size(q2x,1),1) q2x];
y = q2y;
%% linear regression
theta = pinv(x'*x)*x'*y;
figure;

hold on;
plot(x(:,2),y,'.b');
regr_line_x = min(x(:,2)):.1:max(x(:,2));
regr_line_y = theta(2)*regr_line_x + theta(1);
plot(regr_line_x,regr_line_y,'b');
%% locally weighted linear regression
taus = [.1 .3 .8 2 10];
colors = ['r' 'g' 'm' 'y' 'k'];
m = size(q2x,1);
for i=1:size(taus,2)
tau=taus(i);
for k=1:size(regr_line_x,2)
W = zeros(m,m);
for l=1:m
W(l,l)=exp(-(regr_line_x(k)-x(l,2))^2/(2*tau^2));
end
theta = pinv(x'*W*x)*x'*W*y;
regr_line_y(k) = theta(2)*regr_line_x(k) + theta(1);
end
plot(regr_line_x,regr_line_y,colors(i));
end

legend('trainingdata','linear','tau=.1','tau=.3',...
'tau=.8','tau=2','tau=10')
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%