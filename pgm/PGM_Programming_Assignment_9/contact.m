function [t] = contact(t1, t2)
%CONTACT Summary of this function goes here
%   Detailed explanation goes here
t = t1;
for i=1:3
    s1 = t1(i);
    s2 = t2(i);
    m = size(s1.poseData, 1);
    pair_m = size(s1.InitialPairProb, 1);
    n = size(s2.poseData, 1);
    for j=1:length(s2.actionData)
        s2.actionData(j).marg_ind = s2.actionData(j).marg_ind + m;
        s2.actionData(j).pair_ind = s2.actionData(j).pair_ind + pair_m;
    end
    s1.actionData = [s1.actionData s2.actionData];

    s1.poseData = [s1.poseData; s2.poseData];
    s1.InitialClassProb = [s1.InitialClassProb; s2.InitialClassProb ];
    s1.InitialPairProb = [s1.InitialPairProb; s2.InitialPairProb];
    t(i) = s1;
end
end

