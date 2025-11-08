"""
3. Longest Substring Without Repeating Characters
https://leetcode.com/problems/longest-substring-without-repeating-characters/
Difficulty: Medium

Given a string s, find the length of the longest substring without repeating characters.

Time complexity: O(n^2)
Space complexity: O(n)

Note: This is a brute force solution. See p0003_longest_substring_v2.py for optimized O(n) version.
"""

from typing import List


class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        if len(s) == 1:
            return 1

        ans = []
        output = 0
        for i in range(len(s) - 1):
            ans.append(s[i])
            for j in range(i + 1, len(s)):
                if s[j] in ans:
                    if output <= len(ans):
                        output = len(ans)
                    ans = []
                    break
                else:
                    ans.append(s[j])
                    if j == len(s) - 1 and output <= len(ans):
                        output = len(ans)
            ans = []
        return output


# Test cases
test_cases = [
    {"input": {"s": "abcabcbb"}, "expected": 3},
    {"input": {"s": "bbbbb"}, "expected": 1},
    {"input": {"s": "pwwkew"}, "expected": 3},
    {"input": {"s": "au"}, "expected": 2},
    {"input": {"s": " "}, "expected": 1},
]
