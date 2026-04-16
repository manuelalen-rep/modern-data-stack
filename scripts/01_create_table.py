import psycopg2

# Conexión con los datos que definiste
conn = psycopg2.connect(
    host="localhost",
    database="modern_data_stack",
    user="admin", # Usamos admin para crear la tabla inicial
    password="password123"
)

cur = conn.cursor()

# SQL estilo SAP para producción de ropa
create_table_sql = """
CREATE TABLE IF NOT EXISTS bronze.zt_prod_clothing (
    mandt           CHAR(3),          -- Mandante
    aufnr           VARCHAR(12) PRIMARY KEY,      -- Orden de fabricación
    matnr           VARCHAR(18),      -- SKU Final (ej: PANT-JEAN-BLUE-L)
    cmp_matnr       VARCHAR(18),      -- Parte (ej: ZIPPER-YKK-15)
    werks           CHAR(4),          -- Fábrica (Plant)
    vornr           CHAR(4),          -- Operación (ej: 0010 - Corte)
    ltxa1           VARCHAR(40),      -- Descripción (ej: Cosido de cremallera)
    start_time      TIMESTAMP,        -- Inicio real
    end_time        TIMESTAMP,        -- Fin real
    target_time_min DECIMAL(10,2),    -- Tiempo estándar
    actual_time_min DECIMAL(10,2),    -- Tiempo real calculado
    ersda           DATE DEFAULT CURRENT_DATE, -- Fecha creación
    updated_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""

cur.execute(create_table_sql)
conn.commit()
cur.close()
conn.close()
print("¡Tabla de SAP creada exitosamente en el esquema Bronze!")