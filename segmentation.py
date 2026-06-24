
import sqlite3
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans 
import joblib

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



final_kmeans=KMeans(n_clusters=3,random_state=42,n_init=10)
cluster_labels=final_kmeans.fit_predict(scaled_df)
rfm_df['Cluster']=cluster_labels




seg_map={
    0:'New/Promissing',
    1:'Champions',
    2:'At-Risk'
}
rfm_df['Segment']=rfm_df['Cluster'].map(seg_map)


conn=sqlite3.connect('ecommerce.db')
output_df=rfm_df[['user_id','Segment']]
output_df.to_sql('user_segments', conn ,if_exists='replace',index=False)

conn.commit()
conn.close()



joblib.dump(scaler,'rfm_scaler.joblib')
joblib.dump(final_kmeans,'kmeans_model.joblib')

