# 🏭 Modern Data Stack - SAP Clothing Production Pipeline

Este repositorio contiene una prueba de concepto (PoC) de una arquitectura **Modern Data Stack** local de extremo a extremo. Simula la ingesta, almacenamiento y transformación de datos de producción de ropa (estilo SAP ERP) utilizando las mejores herramientas del mercado.

## 🛠️ Stack Tecnológico

* **Orquestación:** Apache Airflow
* **Infraestructura como Código (IaC):** Terraform
* **Data Lake (Local):** Azurite (Emulador de Azure Blob Storage)
* **Data Warehouse:** PostgreSQL
* **Transformación de Datos:** dbt (Data Build Tool)
* **Contenedores:** Docker & Docker Compose
* **Lenguaje:** Python & SQL

## 🏗️ Arquitectura del Pipeline

El flujo de datos (DAG en Airflow) sigue estos pasos:
1.  **Generación de Datos (Simulación SAP):** Scripts en Python generan datos aleatorios de órdenes de producción y los suben al Data Lake (Azurite) en la capa `raw`.
2.  **Ingesta (Bronze):** Airflow lee los archivos CSV más recientes de Azurite y los ingesta tal cual en la base de datos PostgreSQL (esquema `bronze`).
3.  **dbt Source Freshness:** Se verifica que los datos en `bronze` no estén obsoletos.
4.  **dbt Tests:** Se aplican pruebas de calidad (Primary Keys, Not Nulls).
5.  **Transformación (Silver/Gold):** dbt transforma los datos crudos en modelos analíticos listos para el negocio.

---

## 🚀 Guía de Instalación y Ejecución

Sigue estos pasos rigurosamente para levantar el entorno desde cero sin errores de dependencias.

### Prerrequisitos
* [Docker Desktop](https://www.docker.com/products/docker-desktop/) instalado y corriendo.
* [Terraform](https://developer.hashicorp.com/terraform/downloads) instalado.
* Python 3.10+ (Para ejecutar los scripts generadores).
* **⚠️ IMPORTANTE:** Si usas Visual Studio Code, asegúrate de **DESACTIVAR la extensión de Azurite** antes de empezar, ya que creará conflictos con el puerto `10000` de Docker.

### Paso 1: Limpieza del entorno
Asegúrate de no tener contenedores antiguos o bases de datos "sucias" de pruebas anteriores:
```bash
docker-compose down -v --remove-orphans
