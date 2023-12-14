# ネットワークの中心性計算
# 次数中心性(degree centrality)
# 固有ベクトル中心性(Eigenvector centrality)
# ページランク(PageRank)
# 媒介中心性(Betweeness centrality)
# 情報中心性(Information centrality)


class NetworkCentrality:
    """
    ネットワークの中心性計算用アルゴリズム
    networkX内にパッケージがあるものだけ集めた
    """

    def __init__(self, graph: nx.Graph) -> None:
        self.graph = graph

    def calc_degree_centrality(self):
        pass
    def calc_eigenvector_centrality(self):
        pass

    def calc_closeness_centrality(self):
        pass

    def calc_current_flow_closeness(self):
        pass

    def calc_betweeness_centrality(self):
        pass

    def calc_current_flow_betweenness(self):
        pass

    def calc_communicability_betweenness(self):
        pass

    def calc_group_centrality(self):
        pass

    def calc_pagerank(self):
        pass

    def calc_information_centrality(self):
        pass
