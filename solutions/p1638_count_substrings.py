"""
1638. Count Substrings That Differ by One Character
https://leetcode.com/problems/count-substrings-that-differ-by-one-character
Difficulty: Medium

Given two strings s and t, find the number of ways you can choose a non-empty
substring of s and replace a single character by a different character such that
the resulting substring is a substring of t.

Return the number of substrings that satisfy the condition above.

Time complexity: O(n^3)
Space complexity: O(1)
"""

from typing import List


class Solution:
    def countSubstrings(self, s: str, t: str) -> int:
        out = 0
        i_size = len(s)
        j_size = len(t)
        w_size = max(len(s), len(t))

        for w in range(1, w_size + 1):
            for i in range(i_size):
                if i + w > i_size:
                    continue
                for j in range(j_size):
                    if j + w > j_size:
                        continue
                    out += self.compareSubstrings(s[i : i + w], t[j : j + w])

        return out

    def compareSubstrings(self, x: str, y: str) -> int:
        """Check if two substrings differ by exactly one character."""
        is_equal = 0

        if len(x) != len(y):
            return is_equal

        for i in range(len(x)):
            if x[i] != y[i]:
                is_equal += 1

        return is_equal == 1


test_cases = [
    {"input": {"s": "aba", "t": "baba"}, "expected": 6},
    {"input": {"s": "ab", "t": "bb"}, "expected": 3},
    {"input": {"s": "a", "t": "a"}, "expected": 0},
    {"input": {"s": "abe", "t": "bbc"}, "expected": 10},
]
