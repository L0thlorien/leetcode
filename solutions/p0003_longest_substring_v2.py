"""
3. Longest Substring Without Repeating Characters
https://leetcode.com/problems/longest-substring-without-repeating-characters/
Difficulty: Medium

Given a string s, find the length of the longest substring without repeating characters.

Time complexity: O(n)
Space complexity: O(n)

This is an optimized sliding window solution.
"""

from typing import List


class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        seen = []
        left = 0
        max_len = 0

        for right in range(len(s)):
            while s[right] in seen:
                seen.remove(s[left])
                left += 1
            seen.append(s[right])
            max_len = max(max_len, right - left + 1)

        return max_len


test_cases = [
    {"input": {"s": "abcabcbb"}, "expected": 3},
    {"input": {"s": "bbbbb"}, "expected": 1},
    {"input": {"s": "pwwkew"}, "expected": 3},
    {"input": {"s": "au"}, "expected": 2},
    {"input": {"s": " "}, "expected": 1},
]
