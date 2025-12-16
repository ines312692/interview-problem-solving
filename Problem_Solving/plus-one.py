from typing import List


class Solution:
    def plusOne(self, digits: List[int]) -> List[int]:
        n = len(digits)

        # Start from the last digit
        for i in range(n - 1, -1, -1):
            if digits[i] < 9:
                digits[i] += 1
                return digits
            digits[i] = 0  # If it's 9, it becomes 0 and we carry 1 to the next digit

        # If all digits were 9, we need an extra 1 at the front
        return [1] + [0] * n