"""
good solution for
3. Longest Substring Without Repeating Characters
https://leetcode.com/problems/longest-substring-without-repeating-characters/
Time complexity: O(n)
Space complexity: O(n)
"""
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


def main():
    test_case = 'pwwkew'
    sol = Solution()
    print(sol.lengthOfLongestSubstring(test_case))

if __name__ == '__main__':
    main()
