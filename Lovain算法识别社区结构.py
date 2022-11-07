import random
import networkx as nx
import networkx.algorithms.community as nx_comm
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics import normalized_mutual_info_score
import scipy.stats as ss
import add

df = pd.read_excel('./案例数据/MI.xlsx')
BNSS = list(df.columns)
G = nx.complete_graph(BNSS)


for u,v,d in G.edges(data=True):
     d['weight'] = normalized_mutual_info_score(df[u],df[v])
weight_BNSS = list(nx.get_edge_attributes(G,'weight').values())

edgewidth = [weight_BNSS[i]*3 for i in range(len(BNSS)) ]





nx_att = {
    'font_size':5,
    'node_size':300,
    'edge_color':'#DCDCDC',
    'width':edgewidth,
    'alpha':0.7
}




communities = nx_comm.louvain_communities(G, weight="weight", resolution=1, threshold=0.000000001, seed=None)

print(list(communities))
community_dict = {}
community_num = 0
community_color = {}
color_dict ={}

for community in communities:
    # 对每个社区随机生成颜色参数
    community_color[community_num]=random.randint(0,255)
    for node in community:
        # 构建{节点：所属社区}字典
        community_dict[node] = community_num
        # 为图中每个点添加一个 community 属性，该属性值记录该点所在的社区编号
        nx.set_node_attributes(G, community_dict, 'community')
        # 构建{节点：节点颜色}
        color_dict[node] = community_color[community_num]
        # 为图中每个点添加一个 color 属性，该属性值记录该点的颜色
        nx.set_node_attributes(G, color_dict, 'color')

    community_num += 1

# 计算社团内部边数（连接节点到其社区内其他节点的边的和）
inter_degree = list(add.communities_inter_degree(G,communities).values())

# 计算社团外部边数（连接节点与来自其他社区的节点的边之和）
outer_degree = list(add.communities_outer_degree(G,communities).values())



print(ss.ranksums(outer_degree,inter_degree))

node_color = list(nx.get_node_attributes(G,'color').values())
nx.draw_networkx(G,node_color=node_color,**nx_att)
plt.show()

