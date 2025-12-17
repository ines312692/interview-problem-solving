class Solution:
    def summaryRanges(self, nums: List[int]) -> List[str]:
        ranges = []
        i = 0
        n = len(nums)

        while i < n:
            start = nums[i]
            # avancer tant que le nombre suivant est consécutif
            while i + 1 < n and nums[i + 1] == nums[i] + 1:
                i += 1
            end = nums[i]
            # ajouter la chaîne correcte
            if start == end:
                ranges.append(str(start))
            else:
                ranges.append(f"{start}->{end}")
            i += 1

        return ranges
