def matrix_chain_order(p):
    n = len(p) - 1
    m = [[0 if i==j else 0 for i in range(n)] for j in range(n)]
    s = [[0 for i in range(n)] for j in range(n)]

    for l in range(2,n+1):
        for i in range(n - l + 1):
            j = i + l - 1
            m[i][j] = 10000000
            for k in range(i, j):
                q = m[i][k] + m[k+1][j] + p[i]*p[k+1]*p[j+1]
                if q < m[i][j]:
                    m[i][j] = q
                    s[i][j] = k

    print m[0][n-1]
    print_optimal_parens(s, 0, n -1)

def print_optimal_parens(s, i, j):
    if i == j:
        print 'A'+ str(i),
    else:
        print '(',
        print_optimal_parens(s, i, s[i][j])
        print_optimal_parens(s, s[i][j]+1, j)
        print ')',

p = [30,35,15,5,10,20,25]
matrix_chain_order(p)



