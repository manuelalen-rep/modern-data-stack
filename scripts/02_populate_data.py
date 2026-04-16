import pandas as pd
import random
from datetime import datetime
from azure.storage.blob import BlobServiceClient
from azure.core.exceptions import ResourceExistsError

CONN_STR = "DefaultEndpointsProtocol=http;AccountName=devstoreaccount1;AccountKey=Eby8vdM02xNOcqFlqUwJPLlmEtlCDXJ1OUzFT50uSRZ6IFsuFq2UVErCz4I6tq/K1SZFPTOtr/KBHBeksoGMGw==;BlobEndpoint=http://127.0.0.1:10000/devstoreaccount1;"

def generate_random_data(n_rows=10):
    skus = ['JEANS-001', 'SHIRT-002', 'BELT-003', 'JACKET-004', 'SOCKS-005']
    components = {'JEANS-001': ['ZIPPER-YKK', 'DENIM-BLUE'], 'SHIRT-002': ['COTTON-WHITE'], 'BELT-003': ['BUCKLE-STEEL'], 'JACKET-004': ['LEATHER-BLACK'], 'SOCKS-005': ['WOOL-RED']}
    rows = []
    today_str = datetime.now().strftime("%Y-%m-%d")
    for _ in range(n_rows):
        matnr = random.choice(skus)
        rows.append({
            'mandt': '100', 'aufnr': f"100{random.randint(1000, 9999)}",
            'matnr': matnr, 'cmp_matnr': random.choice(components[matnr]),
            'werks': 'ES01', 'target_time_min': 10.0, 'actual_time_min': 12.0, 'ersda': today_str
        })
    return pd.DataFrame(rows)

def upload_to_azurite():
    print("--- Iniciando proceso de carga ---")
    try:
        blob_service_client = BlobServiceClient.from_connection_string(CONN_STR)
        print("✅ Cliente conectado con Connection String.")

        for c in ["exchange", "raw"]:
            try:
                blob_service_client.create_container(c)
                print(f"✅ Contenedor '{c}' creado.")
            except ResourceExistsError:
                print(f"ℹ️ Contenedor '{c}' ya existía.")

        df = generate_random_data(10)
        csv_content = df.to_csv(index=False)
        
        now = datetime.now()
        blob_name = f"{now.strftime('%Y/%m/%d')}/produccion_{now.strftime('%H%M%S')}.csv"

        blob_client = blob_service_client.get_blob_client(container="raw", blob=blob_name)
        blob_client.upload_blob(csv_content, overwrite=True)
        
        print("🚀 ¡ÉXITO! Archivo subido correctamente al Lake.")

    except Exception as e:
        print(f"❌ ERROR: {e}")

if __name__ == "__main__":
    upload_to_azurite()