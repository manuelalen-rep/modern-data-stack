from azure.storage.blob import BlobServiceClient
import pandas as pd
from datetime import datetime

conn_str = "UseDevelopmentStorage=true"

def inicializar_lago():
    print("--- Inicializando Azurite ---")
    try:
        client = BlobServiceClient.from_connection_string(conn_str)

        for container in ["raw", "exchange"]:
            try:
                client.create_container(container)
                print(f"✅ Contenedor '{container}' creado con éxito.")
            except Exception as e:
                if "ContainerAlreadyExists" in str(e):
                    print(f"✅ Contenedor '{container}' ya existía.")
                else:
                    print(f"⚠️ No se pudo crear '{container}': {e}")

        now = datetime.now()
        blob_name = f"{now.strftime('%Y/%m/%d')}/archivo_inicial.csv"
        container_client = client.get_container_client("raw")
        
        print(f"📤 Creando estructura de carpetas subiendo: {blob_name}...")

        df = pd.DataFrame({"inicializacion": ["ok"]})
        csv_data = df.to_csv(index=False)
        
        container_client.upload_blob(name=blob_name, data=csv_data, overwrite=True)
        print("🚀 ¡Azurite inicializado y listo! El contenedor 'raw' ya existe.")
        
    except Exception as e:
        print(f"❌ ERROR FATAL: {e}")

if __name__ == "__main__":
    inicializar_lago()