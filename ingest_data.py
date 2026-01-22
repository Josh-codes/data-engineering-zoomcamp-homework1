#!/usr/bin/env python
# coding: utf-8


import pandas as pd
from sqlalchemy import create_engine
from tqdm.auto import tqdm
import click
import pyarrow.parquet as pq
import urllib.request
import os



# Green taxi parquet URL
PARQUET_URL = 'https://d37ci6vzurychx.cloudfront.net/trip-data/green_tripdata_2025-11.parquet'



@click.command()
@click.option('--pg-user', default='postgres', help='PostgreSQL user')
@click.option('--pg-pass', default='postgres', help='PostgreSQL password')
@click.option('--pg-host', default='localhost', help='PostgreSQL host')
@click.option('--pg-port', default='5432', help='PostgreSQL port')
@click.option('--pg-db', default='ny_taxi', help='PostgreSQL database name')
@click.option('--url', default=PARQUET_URL, help='URL of the parquet file')
@click.option('--chunksize', default=100000, type=int, help='Chunk size for processing')
@click.option('--target-table', default='green_taxi_data', help='Target table name')
def run(pg_user, pg_pass, pg_host, pg_port, pg_db, url, chunksize, target_table):

    # Download parquet file
    parquet_filename = url.split('/')[-1]
    parquet_path = f'/tmp/{parquet_filename}'
    
    if not os.path.exists(parquet_path):
        print(f'Downloading {url}...')
        urllib.request.urlretrieve(url, parquet_path)
        print(f'Downloaded to {parquet_path}')
    else:
        print(f'Using existing file: {parquet_path}')

    engine = create_engine(f'postgresql://{pg_user}:{pg_pass}@{pg_host}:{pg_port}/{pg_db}')

    # Read parquet file
    parquet_file = pq.ParquetFile(parquet_path)
    
    first = True
    for batch in tqdm(parquet_file.iter_batches(batch_size=chunksize)):
        df_chunk = batch.to_pandas()
        if first:
            df_chunk.head(n=0).to_sql(
                name=target_table, 
                con=engine, 
                if_exists='replace'
            )
            first = False
        df_chunk.to_sql(
            name=target_table, 
            con=engine, 
            if_exists='append'
        )
    
    print(f'Finished ingesting data into {target_table}')


if __name__ == '__main__':
    run()



