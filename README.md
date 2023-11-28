# Working with large datasets with Pandas and SQlite 

# Preare your working directory

Create a working directory and download the IMDB non-commerical dataset

Details of the dataset can be found at https://developer.imdb.com/non-commercial-datasets/

You can download the complete dataset as follows, these data files are in compressed
format, so we uncompress them using the gunzip command at the end:

```
wget https://datasets.imdbws.com/name.basics.tsv.gz
wget https://datasets.imdbws.com/title.akas.tsv.gz
wget https://datasets.imdbws.com/title.basics.tsv.gz
wget https://datasets.imdbws.com/title.crew.tsv.gz
wget https://datasets.imdbws.com/title.episode.tsv.gz
wget https://datasets.imdbws.com/title.principals.tsv.gz
wget https://datasets.imdbws.com/title.ratings.tsv.gz
gunzip *.gz
```

# Exercise 1

The file `name.basics.tsv` contains all the names of everyone that works in
the entertainment industry.

Write a python function to output the number of dead actors that were born
after the year 2000.

I want 2 versions: one using the csv module and the other using pandas.

## LESSON

Pandas, by default, will read the entire dataset into memory.  In
case when there is not enough memory, the process will be killed.

In contrast, the csv (or even python open()) version will work fine,
because the for loop only process one line at a time.

# Exercise 2

The file title.principals.tsv list out all the major workers for each
of the entertainment titles.  Write 2 python functions using the csv
technique and the pandas technique to extract all the unique job categories.

```
def count_jobs():
    chunks = pd.read_csv('title.principals.tsv', delimiter='\t', chunksize=50000)

    jobs = []
    for df in chunks:
        jobs = jobs + list(df['category'].unique())

    return set(jobs)
```

# Exercise 3

The chunk method is ok, but the issue is you are doing a lot of work in python
manipulating lists inside python.  We can use to_sql() function of pandas
to write the data into sqlite databse, then we can use the SQL language
to extract only the data we want.

Instead, what we can do is write each record into a SQL database, which is
optimitized for operating on large datasets without reading everything into
memory.

Pandas has built-in ability to work with SQL databases.  The following
python code will read all data from title.principals.tsv and write it to
a file called imdb.db:

```
import pandas
import sqlite3

def write_to_sqlite():
    chunks = pd.read_csv('title.principals.tsv', delimiter='\t', chunksize=50000)
    conn = sqlite3.connect('imdb.db')
    for df in chunks:
        df.to_sql('principals', conn, if_exists='append')

```

After the above code is executed (will have to wait a few minutes), the file
imdb.db will be created in your working directory.  You can inspect the
imdb.db database using the `sqlite3` command in the bash shell:

```
$ sqlite3 imdb.db
SQLite version 3.37.2 2022-01-06 13:25:41
Enter ".help" for usage hints.
sqlite> select * from principals limit 10;
0|tt0000001|1|nm1588970|self|\N|["Self"]
1|tt0000001|2|nm0005690|director|\N|\N
2|tt0000001|3|nm0374658|cinematographer|director of photography|\N
3|tt0000002|1|nm0721526|director|\N|\N
4|tt0000002|2|nm1335271|composer|\N|\N
5|tt0000003|1|nm0721526|director|\N|\N
6|tt0000003|2|nm1770680|producer|producer|\N
7|tt0000003|3|nm1335271|composer|\N|\N
8|tt0000003|4|nm5442200|editor|\N|\N
9|tt0000004|1|nm0721526|director|\N|\N
```

In the above interaction, we enter into the sqlite console, then execute
a query to inspect the first 10 records of the table `principals`, which
we created from the python code.

The following SQL command (we actually call it SQL Query) will retrieve
all unique job categories:

```
sqlite> select distinct(category) from principals;
self
director
cinematographer
composer
producer
editor
actor
actress
writer
production_designer
archive_footage
archive_sound
```

We can actually execute SQL from pandas, like this:

```
def count_jobs_sql():
    conn = sqlite3.connect('imdb.db')
    df = pd.read_sql('select distinct(category) from principals', conn)
    return df

```

# Exercise 4

Now is a good time to learn some SQL basics, complete the following tutorials:

https://sqlzoo.net/wiki/SELECT_basics

https://sqlzoo.net/wiki/SELECT_from_WORLD_Tutorial

https://sqlzoo.net/wiki/SELECT_from_Nobel_Tutorial

https://sqlzoo.net/wiki/SELECT_within_SELECT_Tutorial
