class Solution:
    def nextPermutation(self, nums: List[int]) -> None:
        n = len(nums)
        i = n - 2

        # Étape 1 : trouver le pivot
        while i >= 0 and nums[i] >= nums[i+1]:
            i -= 1

        if i >= 0:
            # Étape 2 : trouver le successeur
            j = n - 1
            while nums[j] <= nums[i]:
                j -= 1
            # Étape 3 : échanger pivot et successeur
            nums[i], nums[j] = nums[j], nums[i]

        # Étape 4 : inverser la partie droite du pivot
        left, right = i + 1, n - 1
        while left < right:
            nums[left], nums[right] = nums[right], nums[left]
            left += 1
            right -= 1
