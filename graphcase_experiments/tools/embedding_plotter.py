from math import pi, cos, sin
import networkx as nx
import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd
import numpy as np
from sklearn.manifold import MDS

def plot_embedding(G, embed, path=None):
    # reduce dimensions of embeding to two
    if embed.shape[1] > 3:
        mds = MDS(n_components=2)
        ids = embed[:,0]
        embed = mds.fit_transform(embed[:,1:])
        embed = np.column_stack([ids, embed])

    fig, ax = plt.subplots(1,1)
    # plot embeding
    embed_df = pd.DataFrame(embed, columns=['id', 'embed1', 'embed2'])
    lbl_df = pd.DataFrame(
        [[i,x] for i,x in nx.get_node_attributes(G,'label').items()],
        columns=['id', 'label']
    )
    embed_df = pd.merge(embed_df, lbl_df, on='id', how='inner')

    labels = [x for _,x in nx.get_node_attributes(G,'label').items()]
    labels.sort()
    tmp = {n:i for i,n in enumerate(list(dict.fromkeys(labels)))}
    label_dic = {k:v/(len(tmp.values())-1) for k,v in tmp.items()}
    color = [label_dic[x] for _, x in embed_df['label'].items()]
  
    ax.scatter(embed_df['embed1'], embed_df['embed2'], s=20., c=color, cmap=plt.cm.rainbow)

    # add legend and title 
    markers = [plt.Line2D([0,0],[0,0], color=plt.cm.rainbow(c), marker='o', linestyle='') for c in label_dic.values()]
    plt.legend(markers, label_dic.keys(), numpoints=1, loc=(1.04,0))
    ax.set_xlabel("dim1")
    ax.set_ylabel("dim2")
    plt.title("Barbel graph: node coler represents the node role, label = node id")
    
    # save fig
    if path:
        fig.savefig(path + 'embed_plot_graphCASE.png', dpi=300, format='png')
    plt.show()

def plot_embedding2(pdf, path=None):
    # reduce dimensions of embeding to two
    cols = [c for c in pdf.columns if c.startswith('embed')]
    if pdf.shape[1] > 5:
        mds = MDS(n_components=2)
        embed_df = pdf[['id', 'label', 'label_id']]
        embed = mds.fit_transform(pdf[cols].values)
        embed_df['embed1'] = embed[:,0]
        embed_df['embed2'] = embed[:,1]
    else:
        embed_df = pdf

    color_tbl = embed_df[['label','label_id']].drop_duplicates()
    color_cnt = color_tbl.shape[0]

    # plot embeding
    fig, ax = plt.subplots(1,1)

  
    ax.scatter(embed_df['embed1'], embed_df['embed2'], s=20., c=embed_df['label_id']/color_cnt, cmap=plt.cm.rainbow)

    # add legend and title 
    
    markers = [plt.Line2D([0,0],[0,0], color=plt.cm.rainbow(r['label_id']/color_cnt), marker='o', linestyle='') for i,r  in color_tbl.iterrows()]
    plt.legend(markers, color_tbl['label'], numpoints=1, loc=(1.04,0))
    ax.set_xlabel("dim1")
    ax.set_ylabel("dim2")
    plt.title("Barbel graph: node coler represents the node role, label = node id")
    
    # save fig
    if path:
        fig.savefig(path + 'embed_plot_graphCASE.png', dpi=300, format='png')
    plt.show()

import plotly.express as px
def plotly_embedding(pdf, path=None):
    # reduce dimensions of embeding to two
    cols = [c for c in pdf.columns if c.startswith('embed')]
    if pdf.shape[1] > 5:
        mds = MDS(n_components=2)
        embed_df = pdf[['id', 'label', 'label_id']]
        embed = mds.fit_transform(pdf[cols].values)
        embed_df['embed1'] = embed[:,0]
        embed_df['embed2'] = embed[:,1]
    else:
        embed_df = pdf

    color_tbl = embed_df[['label','label_id']].drop_duplicates()
    color_cnt = color_tbl.shape[0]

    # plot embeding
    fig = px.scatter(embed_df, x="embed1", y="embed2", color="label", hover_data=['id', 'label'])


    # add legend and title 
    
    # markers = [plt.Line2D([0,0],[0,0], color=plt.cm.rainbow(r['label_id']/color_cnt), marker='o', linestyle='') for i,r  in color_tbl.iterrows()]
    # plt.legend(markers, color_tbl['label'], numpoints=1, loc=(1.04,0))
    # ax.set_xlabel("dim1")
    # ax.set_ylabel("dim2")
    # plt.title("Barbel graph: node coler represents the node role, label = node id")
    fig.show()