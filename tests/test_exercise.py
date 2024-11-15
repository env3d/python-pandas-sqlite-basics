import pytest
from unittest.mock import mock_open, patch
import io
import pandas as pd
import sqlite3
import os
import sys

# Add the parent directory to sys.path
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, parent_dir)
from main import *

# Mock data for the name.basics.tsv file
mock_name_basics_data = """nconst\tprimaryName\tbirthYear\tdeathYear\tprimaryProfession\tknownForTitles
nm0000001\tActor One\t2001\t2020\tactor\ttt0000001
nm0000002\tActor Two\t1999\t2020\tactor\ttt0000002
nm0000003\tYoung Actor\t2003\t2019\tactor\ttt0000003
nm0000004\tOlder Actor\t1980\t\\N\tactor\ttt0000004
nm0000005\tAnother Actor\t2005\t2021\tactor,producer\ttt0000005
"""

# Mock data for the title.principals.tsv file
mock_title_principals_data = """tconst\tordering\tnconst\tcategory\tjob\tcharacters
tt0000001\t1\tnm0005690\tdirector\t\\N\t\\N
tt0000002\t1\tnm0374658\tactor\t\\N\t\\N
tt0000003\t1\tnm0005690\tcinematographer\t\\N\t\\N
tt0000004\t1\tnm1335271\tcomposer\t\\N\t\\N
tt0000005\t1\tnm0005690\tactor\t\\N\t\\N
"""

# Test for count_dead_actor_csv using mock data
def test_count_dead_actors_csv():
    with patch("builtins.open", mock_open(read_data=mock_name_basics_data)):
        result = count_dead_actors_csv()
        assert result == 3  # Two actors born after 2000 with a death year

# Test for count_dead_actor_pandas using mock data
def test_count_dead_actors_pandas():
    with patch("builtins.open", mock_open(read_data=mock_name_basics_data)):
        result = count_dead_actors_pandas()
        assert result == 3  # Two actors born after 2000 with a death year

# Test for count_jobs using mock data and pandas chunking
def test_get_jobs_csv():
    with patch("builtins.open", mock_open(read_data=mock_title_principals_data)):
        result = get_jobs_csv()
        assert result == {"director", "actor", "cinematographer", "composer"}

# Test for count_jobs using mock data and pandas chunking
def test_get_jobs_pandas():
    with patch("builtins.open", mock_open(read_data=mock_title_principals_data)):
        result = get_jobs_pandas()
        assert result == {"director", "actor", "cinematographer", "composer"}

# Fixture to mock file reading and set up an in-memory SQLite database
@pytest.fixture(scope="module")
def get_db_name():
    yield "_imdb_.db"
    os.remove("_imdb_.db")


# Test for write_to_sqlite using the setup fixture
def test_write_to_sqlite(get_db_name):
    conn = sqlite3.connect(get_db_name)
    with patch("builtins.open", mock_open(read_data=mock_title_principals_data)):
        with patch("sqlite3.connect", return_value=conn):
            write_to_sqlite()  # Writes data to the in-memory SQLite db

        # Verify the data was written correctly
        conn2 = sqlite3.connect(get_db_name)
        cursor = conn2.cursor()
        cursor.execute("SELECT COUNT(*) FROM principals")
        result = cursor.fetchone()[0]
        assert result == 5  # There are 5 entries in the mock title_principals_data

# Test for count_jobs_sql using the setup fixture
def test_get_jobs_sql(get_db_name):
    conn = sqlite3.connect(get_db_name)
    with patch("sqlite3.connect", return_value=conn):
        result = get_jobs_sql()
        assert set(result) == {"director", "actor", "cinematographer", "composer"}


