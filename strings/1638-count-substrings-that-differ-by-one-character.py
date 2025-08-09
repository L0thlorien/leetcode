"""
Given two strings s and t, find the number of ways you can choose a non-empty substring of s and replace a single character by a different character such that the resulting substring is a substring of t. In other words, find the number of substrings in s that differ from some substring in t by exactly one character.

For example, the underlined substrings in "computer" and "computation" only differ by the 'e'/'a', so this is a valid way.

Return the number of substrings that satisfy the condition above.

A substring is a contiguous sequence of characters within a string.


link: https://leetcode.com/problems/count-substrings-that-differ-by-one-character
"""

class Solution:
    def countSubstrings(s: string, t: string) -> int:
        out = 0
        for i in range(len(s)):

        return out


def main():
    s = 'aba'
    t = 'bba'
    sol = Solution()
    return sol.countSubstrings(s, t)

if __name__ == '__main__':
    main()

