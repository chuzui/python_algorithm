from RollingHash import RollingHash

def longest_substring(s, t):
    """Finds the longest substring that occurs in both s and t"""
    best = ''
    minLen = 0
    maxLen = min(len(s),len(t))
    while minLen <= maxLen:
        length = (minLen + maxLen) / 2
        ans = k_substring(s, t, length)
        if ans is None:
            maxLen = length-1
        else:
            minLen = length + 1
            best = ans
    return best

def k_substring(s, t, k):
    """Finds a substring of length k in both s and t if there is one,
    and returns it. Otherwise, returns None."""
    roll_hs =  RollingHash(256, 9940613)
    roll_ht = RollingHash(256, 9940613)
    hs = {}
    for i in range(k):
        roll_hs.append(ord(s[i]))
        roll_ht.append(ord(t[i]))

    hs[roll_hs.get_value()] = [0];
    for i in range(1, (len(s) - k + 1)):
        roll_hs.append(ord(s[i + k - 1]))
        roll_hs.skip()
        if roll_hs.get_value() in hs:
            hs[roll_hs.get_value()].append(i)
        else:
            hs[roll_hs.get_value()] = [i];



    if roll_ht.get_value() in hs:
        for i in hs[roll_ht.get_value()]:
            if t[0:k] == s[i: i+k]:
                return t[0:k]

    for i in range(1, (len(t) - k + 1)):
        roll_ht.append(ord(t[i + k - 1]))
        roll_ht.skip()
        if roll_ht.get_value() in hs:
            for j in hs[roll_ht.get_value()]:
                if t[i:i+k] == s[j: j+k]:
                    return t[i:i+k]

    return None

print longest_substring("a"*16, "a"*8)