#
# TSPソルバ
# 入力:都市間距離の下三角行列空白区切りのcsvファイル
# 実行時、オプションに入力ファイルパスが必要
# 実行環境python3.7.0
#

# -*- coding: utf-8 -*-
import pulp as pp
import numpy as np
import pprint as pr
import sys

# 最適化モデルの定義
mip_model = pp.LpProblem("tsp_mip", pp.LpMinimize)

#　Nに都市数、c_にiとjの都市間の距離を読み込み
read=[list(map(int,line.rstrip().split(" "))) for line in open(sys.argv[1], 'r').readlines()]
N=read[0][0]
Lower_tri=read[1:]
c_ = [[0] * N for i in range(N)]
for i in range(N):
    for j in range(len(Lower_tri[i])):
        c_[i][j]=Lower_tri[i][j]
        c_[j][i]=Lower_tri[i][j]

#print("Model")
#print(N)
#pr.pprint(c_)

#宣言
x = [[0] * N for i in range(N)]
u = [0] * (N-1)
Hugenum = N

# 変数の定義
for i in range(N):
    for j in range(N):
        if i != j:
            x[i][j] = pp.LpVariable("x(%s,%s)"%(i, j), cat="Binary")

for i in range(N-1):
    u[i] = pp.LpVariable("u(%s)"%(i), cat="Continuous", lowBound=1.0, upBound=N-1)

# 目的関数定義
objective = pp.lpSum(c_[i][j] * x[i][j] for i in range(N) for j in range(N) if i != j)
mip_model += objective

# 移動制約式の登録
for i in range(N):
    mip_model += pp.lpSum(x[i][j] for j in range(N) if i != j) == 1

# 移動制約式の登録
for i in range(N):
    mip_model += pp.lpSum(x[j][i] for j in range(N) if i != j) == 1

# サブツアー制約式
for i in range(N-1):
    for j in range(N-1):
        if i != j:
            mip_model += u[i] + 1.0 - Hugenum * (1.0 - x[i][j]) <= u[j]


# 最適化の実行
status = mip_model.solve()

# 結果の把握
#print("Status")
#print(pp.LpStatus[status])
print(mip_model)

print("Object_value")
print(pp.value(mip_model.objective))
print("Result Route (i,j):moving i to j")
for i in range(len(x)):
    for j in range(len(x[i])):
        if pp.value(x[i][j]) == 1:
            print("(" + str(i) + "," + str(j) + ")")
