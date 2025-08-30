"""
Given two strings s and t, find the number of ways you can choose a non-empty substring of s and replace a single character by a different character such that the resulting substring is a substring of t. In other words, find the number of substrings in s that differ from some substring in t by exactly one character.

For example, the underlined substrings in "computer" and "computation" only differ by the 'e'/'a', so this is a valid way.

Return the number of substrings that satisfy the condition above.

A substring is a contiguous sequence of characters within a string.

link: https://leetcode.com/problems/count-substrings-that-differ-by-one-character

O(n^3) solution

"""


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

    def compareSubstrings(self, x, y):
        is_equal = 0

        if len(x) != len(y):
            return is_equal

        for i in range(len(x)):
            if x[i] != y[i]:
                is_equal += 1

        return is_equal == 1


def main():
    s = "ab"
    t = "bb"
    # s = 'computer'
    # t = 'computation'
    sol = Solution()
    print(sol.countSubstrings(s, t))


if __name__ == "__main__":
    main()
