import csv
import pandas as pd
import sqlite3

# Sample implementations of the functions (uncomment your actual imports above)
def count_dead_actors_csv():
    count = 0
    with open('name.basics.tsv', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file, delimiter='\t')
        for row in reader:
            if row['deathYear'] != '\\N' and int(row['birthYear']) > 2000:
                count += 1
    return count

def count_dead_actors_pandas():
    df = pd.read_csv('name.basics.tsv', delimiter='\t')
    df = df[(df['deathYear'] != '\\N') & (df['birthYear'].astype(int) > 2000)]
    return len(df)

def get_jobs_csv():
    jobs = set()
    with open('title.principals.tsv', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file, delimiter='\t')
        for row in reader:
            jobs.add(row['category'])
    return jobs

def get_jobs_pandas():
    chunks = pd.read_csv('title.principals.tsv', delimiter='\t', chunksize=5000)
    jobs = set()
    for df in chunks:
        jobs.update(df['category'].unique())
    return jobs

def write_to_sqlite():
    chunks = pd.read_csv('title.principals.tsv', delimiter='\t', chunksize=5000)
    conn = sqlite3.connect('imdb.db')
    for df in chunks:
        df.to_sql('principals', conn, if_exists='append', index=False)
    conn.close()

def get_jobs_sql():
    conn = sqlite3.connect('imdb.db')
    df = pd.read_sql('SELECT DISTINCT category FROM principals', conn)
    conn.close()
    return df['category'].unique()
