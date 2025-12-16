class Solution:
    def isPalindrome(self, x: int) -> bool:
        x = str(x)
        i = len(x) - 1
        j = 0

        while j < i:
            if x[i] != x[j]:
                return False
            i -= 1
            j += 1

        return True
