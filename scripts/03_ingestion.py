import os
import pandas as pd
from sqlalchemy import create_engine
from azure.storage.blob import BlobServiceClient
import io

# --- DETECTOR DE ENTORNO ---
# Si existe la variable de entorno de Airflow, sabemos que estamos en Docker
IN_DOCKER = os.environ.get('AIRFLOW_HOME') is not None

# Asignamos los hosts dependiendo de dónde estemos
AZURE_HOST = "azurite" if IN_DOCKER else "127.0.0.1"
PG_HOST = "postgres_db" if IN_DOCKER else "localhost"

# Construimos las cadenas dinámicamente
AZURE_CONN_STR = f"DefaultEndpointsProtocol=http;AccountName=devstoreaccount1;AccountKey=Eby8vdM02xNOcqFlqUwJPLlmEtlCDXJ1OUzFT50uSRZ6IFsuFq2UVErCz4I6tq/K1SZFPTOtr/KBHBeksoGMGw==;BlobEndpoint=http://{AZURE_HOST}:10000/devstoreaccount1;"
PG_CONN_STR = f"postgresql+psycopg2://admin:password123@{PG_HOST}:5432/modern_data_stack"

def ingest_data():
    entorno = "DOCKER (Airflow)" if IN_DOCKER else "WINDOWS (Local)"
    print(f"--- Iniciando Ingesta de Raw a Bronze desde: {entorno} ---")
    
    try:
        # 1. Conectar a Azurite (Data Lake)
        blob_service_client = BlobServiceClient.from_connection_string(AZURE_CONN_STR)
        container_client = blob_service_client.get_container_client("raw")
        
        # 2. Buscar TODOS los archivos en raw
        blobs = list(container_client.list_blobs())
        if not blobs:
            raise ValueError("⚠️ No se encontraron archivos en el contenedor 'raw'. El Lake está vacío.")
        
        # 3. Ordenar y pillar el más reciente
        blobs.sort(key=lambda b: b.creation_time, reverse=True)
        latest_blob = blobs[0]
        print(f"📥 Descargando archivo más reciente: {latest_blob.name}")
        
        # 4. Leer el CSV a memoria
        blob_client = container_client.get_blob_client(latest_blob.name)
        download_stream = blob_client.download_blob()
        df = pd.read_csv(io.BytesIO(download_stream.readall()))
        print(f"📊 Filas preparadas para ingesta: {len(df)}")
        
        # 5. Conectar a Postgres (Data Warehouse)
        engine = create_engine(PG_CONN_STR)

        df.to_sql('zt_prod_clothing', engine, schema='bronze', if_exists='replace', index=False)
        
        print("🚀 ¡ÉXITO! Los datos están por fin en Postgres.")
        
    except Exception as e:
        print(f"❌ ERROR CRÍTICO en la ingesta: {e}")
        raise e

if __name__ == "__main__":
    ingest_data()