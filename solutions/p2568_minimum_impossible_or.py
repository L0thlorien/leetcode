"""
2568. Minimum Impossible OR
https://leetcode.com/problems/minimum-impossible-or/
Difficulty: Medium

You are given a 0-indexed integer array nums.

We say that an integer x is expressible from nums if there exist some integers
0 <= index1 < index2 < ... < indexk < nums.length for which
nums[index1] | nums[index2] | ... | nums[indexk] = x. In other words, an integer
is expressible if it can be written as the bitwise OR of some subsequence of nums.

Return the minimum positive non-zero integer that is not expressible from nums.

Time complexity: O(n)
Space complexity: O(n)
"""

from typing import List


class Solution:
    def minImpossibleOR(self, nums: List[int]) -> int:
        """
        Key insight: The minimum impossible OR must be a power of 2.
        We just need to find the smallest power of 2 not in the array.
        """
        i = 0
        while True:
            if 2 ** i not in nums:
                return 2 ** i
            i += 1


# Test cases
test_cases = [
    {"input": {"nums": [2, 1]}, "expected": 4},
    {"input": {"nums": [5, 3, 2]}, "expected": 1},
    {"input": {"nums": [1, 25, 2, 72]}, "expected": 4},
    {"input": {"nums": [1]}, "expected": 2},
]
