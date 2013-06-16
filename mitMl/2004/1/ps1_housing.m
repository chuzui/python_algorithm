%6.867 Problem Set 1, Fall 2004
clear all;
%load housing data matrix
data=load('housing.data');

%sort matrix according to a single independent variable
for indep_var=1:13
[y,ind]=sort(data(:,indep_var)); %6==no. of rooms
sorted_data{indep_var}=data(ind,:);
end

%plot house price against the sorting variable
plot_feat=13; plotitle=sprintf('%d',plot_feat);
figure;plot(sorted_data{plot_feat}(:,plot_feat),sorted_data{plot_feat}(:,14),'.');title(plotitle);
