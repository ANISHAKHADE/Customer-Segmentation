
import sqlite3
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans 
import joblib
import matplotlib.pyplot as plt
conn=sqlite3.connect('ecommerce.db')
rfm_query="""
SELECT 
   t.user_id,
   CAST(julianday('now')-julianday(MAX(transaction_date)) AS INTEGER ) AS recency,
   COUNT(*) AS frequency,
   SUM(t.quantity * p.price) AS monetary
FROM transactions t
JOIN products p ON t.product_id=p.product_id
GROUP BY  t.user_id
"""

rfm_df=pd.read_sql_query(rfm_query,conn)

conn.close()

features=rfm_df[['recency','frequency','monetary']]
scaler=StandardScaler()
scaled_features=scaler.fit_transform(features)
scaled_df=pd.DataFrame(scaled_features,  columns=features.columns)


inertia_values=[]
cluster_range=range(1,11)
for k in cluster_range:
    kmeans=KMeans(n_clusters=k,random_state=42,n_init=10)
    kmeans.fit(scaled_df)
    inertia_values.append(kmeans.inertia_)


plt.figure(figsize=(8,5))
plt.plot(cluster_range,inertia_values,marker='o',linestyle='--',color='b')
plt.title('The Elbow Method')
plt.xlabel('Number of Clusters (K)')
plt.ylabel('Inertia (WCSS)')
plt.xticks(cluster_range)
plt.grid(True)
plt.show()


final_kmeans=KMeans(n_clusters=3,random_state=42,n_init=10)
cluster_labels=final_kmeans.fit_predict(scaled_df)


seg_map={
    0:'New/Promissing',
    1:'Champions',
    2:'At-Risk'
}
rfm_df['Segment']=rfm_df['Cluster'].map(seg_map)


fig=plt.figure(figsize=(10,8))
ax=fig.add_subplot(111,projection='3d')
colors={'Champions':'gold' , 'New/Promissing':'deepskyblue' , 'At-Risk':'crimson'}

for seg_name, color in colors.items():
    subset=rfm_df[rfm_df['Segment']==seg_name]
    ax.scatter(
        subset['recency'],
        subset['frequency'],
        subset['monetary'],
        c=color,
        label=seg_name,
        s=50,
        alpha=0.8,
        edgecolors='w'
    )

ax.set_xlabel('Recency (Days Ago)')
ax.set_ylabel('Frequency (Total Purchases)')
ax.set_zlabel('Monetary (Total Spend)')
ax.set_title('3D Geometric view of Customer Segments',fontsize=14,pad=20)

plt.legend(title='Customer Segments')
plt.tight_layout()
plt.show()


