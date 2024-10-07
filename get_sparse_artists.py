import os
import pandas as pd

data_files = os.listdir('data')
sparse_artists = []
for file in data_files:
    if file == 'artist_ids.csv':
        continue
    else:
        with open(os.path.join('data', file), 'r') as f:
            songs = f.readlines()
            if len(songs) < 11 : 
                sparse_artists.append(os.path.splitext(file)[0])
sparse_df = pd.DataFrame({'id': sparse_artists})
artist_df = pd.read_csv('data/artist_ids.csv', escapechar='\\').set_index('id')
sparse_df = sparse_df.astype({'id': pd.Int64Dtype()})

sparse_names = sparse_df.join(other=artist_df, on='id', rsuffix='_sparse')
print(sparse_names.head(n=128))