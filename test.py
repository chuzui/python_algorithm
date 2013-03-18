
def binarySearch(array, value):
    l = 0
    r = len(array)
    while l < r:
        mid = (l + r) / 2
        if array[mid] == value:
            return mid
        elif array[mid] > value:
            r = mid - 1
        else:
            l = mid + 1
    return None


x = [2*i+1 for i in range(100)]
print binarySearch(x,37)
