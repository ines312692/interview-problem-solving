from collections import Counter


class Solution:
    def threeSum(self, nums):
        f = Counter(nums)
        res = set()
        if f[0] >= 3:
            res.add((0, 0, 0))

        neg = [x for x in f if x < 0]
        pos = [x for x in f if x > 0]

        for i in neg:
            for j in pos:
                k = -i - j
                if k in f:
                    if (k == i or k == j) and f[k] < 2:
                        continue
                    if k == i and k == j and f[k] < 3:
                        continue
                    res.add(tuple(sorted((i, j, k))))

        for x in f:
            if f[x] >= 2:
                y = -2 * x
                if y != x and y in f:
                    res.add(tuple(sorted((x, x, y))))

        return [list(t) for t in res]