import pandas as pd
from sklearn.neighbors import NearestNeighbors
from sqlalchemy import create_engine

# подключение: если имя пользователя в macOS kikita и без пароля:
engine = create_engine("postgresql+psycopg2://kikita@localhost/spotifykb")

# 1) забираем признаки
df = pd.read_sql("""
    SELECT tf.track_id, tf.danceability, tf.energy, tf.valence, tf.tempo
    FROM track_features tf
""", engine)

if df.empty:
    raise SystemExit("track_features пустая — проверь шаги 3–4.")

X = df[['danceability','energy','valence','tempo']].fillna(0).values

# 2) модель ближайших соседей
K = 10  # топ-10 похожих
nn = NearestNeighbors(n_neighbors=K+1, metric='cosine', algorithm='brute').fit(X)
dist, idx = nn.kneighbors(X)

# 3) собираем результирующую таблицу (пропуская совпадение с самим собой под индексом 0)
rows = []
for i, base in enumerate(df.track_id):
    for j in range(1, K+1):
        sim_id = df.track_id.iloc[idx[i, j]]
        sim = 1 - dist[i, j]  # similarity
        rows.append((base, sim_id, float(sim)))

res = pd.DataFrame(rows, columns=['track_id','similar_track_id','score'])

# 4) пишем в БД (append)
res.to_sql('similar_tracks', engine, if_exists='append', index=False)
print(f"Inserted {len(res)} rows into similar_tracks.")
