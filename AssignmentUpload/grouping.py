import numpy as np
import pandas as pd 
import warnings 
warnings.filterwarnings("ignore")
from sklearn.cluster import KMeans

def groups():
    df = pd.read_csv("StudentsPerformance.csv")
    scores = df.loc[:,["math","physics","chemistry"]]
    wcss = []
    kmeans2 = KMeans(n_clusters = 3)
    clusters = kmeans2.fit_predict(scores)
    scores["cluster_no"] = clusters
    n=len(scores)
    nt=int(n/3)
    result = pd.merge(df,scores,how='left')
    arr0=[]
    arr1=[]
    arr2=[]
    for index, row in result.iterrows():
        if(row['cluster_no']==0):
            arr0.append(row['Name'])
        if(row['cluster_no']==1):
            arr1.append(row['Name'])
        if(row['cluster_no']==2):
            arr2.append(row['Name'])
    l=[]
    teams=[]
    for i in range (nt):
        l.append(arr0[i])
        l.append(arr1[i])
        l.append(arr2[i])
        teams.append(l)
        l=[]
    return teams 
