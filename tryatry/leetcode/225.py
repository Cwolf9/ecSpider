# -*- coding: UTF-8 -*-

"""
@author: Cwolf9
@file: 225
@date: 2021-01-24 13:13
@desc:
"""
from typing import List
import heapq

class Solution:
    def minimumBoxes(self, n: int) -> int:
        val = [1]
        i = 2
        last = val[len(val) - 1]
        while last < n :
            last += i * (i + 1) // 2
            val.append(last)
        l = 1
        r = len(val)
        ans = 1
        while l <= r :
            mid = (l + r) >> 1
            if val[mid - 1] <= n :
                ans = mid
                l = mid + 1
            else :
                r = mid - 1
        return ans * (ans + 1) // 2 + n - val[ans - 1]
tim = int(input())
while tim > 0:
    tim -= 1
    n, m = map(int, input().split())
    n -= m - 3
    if n % 2 == 0:
        if n % 4 == 0:
            a = n // 4
            b = a
            c = n - a - b
        else:
            a = 2
            b = (n - a) // 2
            c = b
    else:
        a = 1
        b = (n - 1) // 2
        c = b
    for i in range(m - 3):
        print(1, end=' ')
    print(a, b, c)