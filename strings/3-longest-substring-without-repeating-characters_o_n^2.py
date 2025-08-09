"""
brootforce solution for
3. Longest Substring Without Repeating Characters
https://leetcode.com/problems/longest-substring-without-repeating-characters/
Time complexity: O(n^2)
Space complexity: O(n)

"""
class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        if len(s) == 1:
            return 1

        ans = []
        output = 0
        for i in range(len(s)-1):
            ans.append(s[i])
            print(f"i: {i}, s[i]:{s[i]}, ans:{ans}")
            for j in range(i+1, len(s)):
                print(f"j: {j}, s[j]:{s[j]}, ans:{ans}")
                if s[j] in ans:
                    print(f"output: {output}")
                    print(f"len ans: {len(ans)}")
                    if output <= len(ans):
                        output = len(ans)
                    print(ans)
                    ans = []
                    break
                else:
                    ans.append(s[j])
                    if j == len(s)-1 and output <= len(ans):
                        output = len(ans)
            ans = []
        return output


def main():
    test_case = 'au'
    sol = Solution()
    print(sol.lengthOfLongestSubstring(test_case))

if __name__ == '__main__':
    main()
