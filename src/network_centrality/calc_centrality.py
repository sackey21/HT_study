import pandas as pd
import networkx as nx

class calc_centrality:
    def calc_group_centrality(gd, gg):


        # 次数中心性（degree centrality）
        gd_degree_centrality = pd.Series(nx.degree_centrality(gd), name="次数中心性")
        gg_degree_centrality = pd.Series(nx.degree_centrality(gg), name="次数中心性")

        # 固有ベクトル中心性：Eigenvector centrality
        gd_eigenvector_centrality = pd.Series(
            nx.eigenvector_centrality(gd, tol=1.0e-3), name="固有ベクトル中心性")
        gg_eigenvector_centrality = pd.Series(
            nx.eigenvector_centrality(gg, tol=1.0e-3), name="固有ベクトル中心性")

        # ページランク：PageRank
        gd_pagerank = pd.Series(nx.pagerank(gd, tol=1.0e-3), name="ページランク")
        gg_pagerank = pd.Series(nx.pagerank(gg, tol=1.0e-3), name="ページランク")

        # 媒介中心性：Betweeness centrality
        gd_betweenness_centrality = pd.Series(
            nx.betweenness_centrality(gd), name="媒介中心性")
        gg_betweenness_centrality = pd.Series(
            nx.betweenness_centrality(gg), name="媒介中心性")

        # 情報中心性：Information centrality
        gg_information_centrality = pd.Series(
            nx.information_centrality(gg), name="情報中心性")

        # 有向グラフ版ランキング（rankを外すと生値が出ます）
        gd_centrality_rank = pd.concat([
            gd_degree_centrality,
            gd_eigenvector_centrality,
            gd_pagerank,
            gd_betweenness_centrality,
        ], axis=1).rank(ascending=False)

        # 無向グラフ版ランキング（rankを外すと生値が出ます）
        gg_centrality_rank = pd.concat([
            gg_degree_centrality,
            gg_eigenvector_centrality,
            gg_pagerank,
            gg_betweenness_centrality,
            gg_information_centrality
        ], axis=1).rank(ascending=False)

        # 中心性が高い順にランキング。値が小さいほど中心に近い。
        print(gd_centrality_rank.loc[gd_centrality_rank.mean(
            axis=1).sort_values().keys()])

        # 中心性が高い順にランキング。値が小さいほど中心に近い。
        print(gg_centrality_rank.loc[gg_centrality_rank.mean(
            axis=1).sort_values().keys()])
