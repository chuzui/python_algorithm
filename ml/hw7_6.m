total =0;
for i=1:10000
    a = rand();
    b = rand();
    total  = total + min(a,b);
end
total / 1000