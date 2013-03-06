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
    print k
    s_substrings = set()
    # Put all substrings of s of length k into a set: s_substrings
    for s_start in range(len(s)-k+1):
        current = s[s_start : s_start+k]
        s_substrings.add(current)
        # For every substring of t of length k, look for it in
    # s_substrings. If it's there, return it.
    for t_start in range(len(t)-k+1):
        current = t[t_start : t_start+k]
        if current in s_substrings:
            return current
    return None

print longest_substring("a"*8, "a"*8)