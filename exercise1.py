
import pandas

def process_py():
    f = open('name.basics.tsv', 'r')

    f.readline()

    i = 0
    collected = []
    for line in f:    
        record = line.split('\t')
        if record[2] != '\\N' and int(record[2]) > 2000 and record[3] != '\\N':
            collected.append(record)

    f.close()
    return collected

def process_pandas():
    chunks = pandas.read_csv('name.basics.tsv', sep='\t', chunksize=5000)
    collected = []
    for df in chunks:
        cleaned = df[ ['primaryName', 'birthYear', 'deathYear'] ].replace('\\N', None).dropna().astype( { 'birthYear': 'int', 'deathYear': 'int' })
        filtered = cleaned[ cleaned['birthYear'] > 2000 ]
        if not filtered.empty:
            collected.append(filtered)
    return pandas.concat(collected)
