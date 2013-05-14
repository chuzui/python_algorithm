k = [2,1,0,-1,-2];

for i = k
    i
    w = line_reg(x_in, y_in, i);
    computeCost(x_out, y_out, w)
end
