# -*- coding: UTF-8 -*-

"""
@author: Cwolf9
@file: ubcf
@date: 2021-04-29 14:50
@desc:
基于用户的协同过滤推荐算法
1. 找到与目标用户兴趣相似的用户集合
2. 找到这个集合中用户喜欢的、并且目标用户没有听说过的物品推荐给目标用户
余弦相似度计算两个用户之间的相似度
https://blog.csdn.net/shixiaoguo90/article/details/80253567
https://www.bilibili.com/video/BV1L5411e7JZ?from=search&seid=6358184118000091269

https://www.zhihu.com/question/29531839
https://zhuanlan.zhihu.com/p/31927875
"""
import math, copy
import utilMysql
from src.model import Users, Goods, Watchlist


class Ubcf:
    """
    user_nid 为离散化用户ID
    d_like[i] 表示用户i喜欢的商品列表
    d_thing[i] 表示喜欢商品i的用户
    w_point[i][j] 表示用户i和j的相似度
    """
    top_k_user = 0
    top_k_good = 0

    def __init__(self, top_k_user=5, top_k_good=10):
        # n 表示用户个数，m 表示商品个数
        self.n, self.m = utilMysql.query('select count(*) from users')[0][0], utilMysql.query('select count(*) from goods')[0][0]
        self.top_k_user, self.top_k_good = min(self.n, top_k_user), min(self.m, top_k_good)
        self.user_nid, self.good_nid = {}, {}
        self.d_like = [[] for i in range(self.n)]
        self.d_thing = [[] for i in range(self.m)]
        self.w_point = [[0]*self.n for i in range(self.n)]
        wls = Watchlist.Watchlist.getWatchlist()
        for wl in wls:
            if wl[0] not in self.user_nid.keys():
                self.user_nid[wl[0]] = len(self.user_nid)
            if wl[1] not in self.good_nid.keys():
                self.good_nid[wl[1]] = len(self.good_nid)
            self.d_like[self.user_nid[wl[0]]].append(self.good_nid[wl[1]])
            self.d_thing[self.good_nid[wl[1]]].append(self.user_nid[wl[0]])

        for x in range(self.m):
            for i in self.d_thing[x]:
                for j in range(i + 1, len(self.d_thing[x])):
                    self.w_point[i][j] += 1
                    self.w_point[j][i] += 1

        for i in range(self.n):
            for j in range(i + 1, self.n):
                if len(self.d_like[i]) * len(self.d_like[j]):
                    self.w_point[i][j] /= math.sqrt(len(self.d_like[i]) * len(self.d_like[j]))
                self.w_point[j][i] = self.w_point[i][j]
            print(self.w_point[i])

    def execute_again(self, top_k_user=5, top_k_good=10):
        self.__init__(top_k_user, top_k_good)

    def get_recommend(self, userid, top_k_user=5, top_k_good=10):
        self.top_k_user, self.top_k_good = min(self.n, top_k_user), min(self.m, top_k_good)
        recommend_list = []
        try:
            # 得到离散化后的用户ID
            new_uid = self.user_nid[userid]
            # 获取用户相似度列表
            user_list = copy.deepcopy(self.w_point[new_uid])
            user_list = [(i, user_list[i]) for i in range(len(user_list))]
            user_list.sort(key=lambda x: x[1], reverse=True)
            print('user_list:\n', user_list)
            # 生成候选商品列表
            candidate_list = []
            for i in range(self.top_k_user):
                for j in self.d_like[user_list[i][0]]:
                    if j not in self.d_like[new_uid] and j not in candidate_list:
                        candidate_list.append([j, 0])
            # 预测喜爱程度
            print('candidate_list:\n', candidate_list)
            for good in candidate_list:
                for user in user_list:
                    if good[0] in self.d_like[user[0]]:
                        good[1] += self.w_point[new_uid][user[0]]
            # 选出top k
            candidate_list.sort(key=lambda x: x[1], reverse=True)
            candidate_list = candidate_list[:min(len(candidate_list), self.top_k_good)]
            candidate_list.sort(key=lambda x: x[0])
            # 根据离散化后的商品ID返回真正的商品ID
            c_index = 0
            for good in self.good_nid.items():
                if c_index < len(candidate_list) and good[1] == candidate_list[c_index][0]:
                    recommend_list.append(good[0])
                    c_index += 1
                    if c_index == len(candidate_list):
                        break
            print(recommend_list)
        except Exception as e:
            print(repr(e))
        finally:
            return recommend_list


if __name__ == '__main__':
    ubcf = Ubcf()
    ubcf.get_recommend(72)