import logging

from tqdm import tqdm
import pandas as pd
from cassandra.cluster import Cluster
from cassandra.concurrent import execute_concurrent_with_args

logging.basicConfig(level=logging.INFO)


def nullable_number(x):
    try:
        return int(x)
    except Exception:
        pass

    return 0


def parse_genres(genres):
    try:
        return genres.split(',')
    except Exception:
        return []


def parse_adult(adult):
    try:
        return bool(adult)
    except Exception:
        logging.warning(f"could parse isAdult={adult}, assume True")
        return True


def main():
    cluster = Cluster()
    session = cluster.connect()

    session.execute(
        "CREATE KEYSPACE IF NOT EXISTS keyspace1 WITH replication={'class':'SimpleStrategy', 'replication_factor':1}")
    session.execute("""CREATE TABLE IF NOT EXISTS keyspace1.movie_data (
        tconst text,
        titleType text,
        primaryTitle text,
        originalTitle text,
        isAdult boolean,
        startYear int,
        endYear int,
        runtimeMinutes int,
        genres list<text>,
        PRIMARY KEY (tconst, startYear)

    ) WITH CLUSTERING ORDER BY (startYear DESC);
    """)

    prepered_insert = session.prepare(
        "INSERT INTO keyspace1.movie_data (tconst, titleType, primaryTitle, originalTitle, isAdult, startYear, endYear, runtimeMinutes, genres)  VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)")

    data = pd.read_csv('title.basics.tsv', sep='\t', dtype=str)

    pbar = tqdm(data.itertuples(), total=len(data.index))
    rows_data = []
    for r in pbar:
        if pd.isna(r.primaryTitle):
            continue

        d = [r.tconst, r.titleType, r.primaryTitle, r.originalTitle, parse_adult(r.isAdult),
             nullable_number(r.startYear), nullable_number(r.endYear),
             nullable_number(r.runtimeMinutes), parse_genres(r.genres)]
        rows_data.append(d)
        if len(rows_data) == 1000:
            try:
                execute_concurrent_with_args(session, prepered_insert, rows_data, concurrency=100)
                rows_data = []
            except Exception:
                # in case of broken data, we try each row on it's own
                for row in rows_data:
                    print(row)
                    session.execute(prepered_insert, row)

    if rows_data:
        execute_concurrent_with_args(session, prepered_insert, rows_data, concurrency=100)


if __name__ == "__main__":
    main()
