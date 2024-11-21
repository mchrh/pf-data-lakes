from common import *
from decimal import Decimal

def ingest_sql_data(spark, sql_file_path, output_path):
    schema = StructType([
        StructField("transaction_id", IntegerType(), False),
        StructField("amount", DecimalType(10, 2), True),
        StructField("customer_name", StringType(), True)
    ])

    try:
        with open(sql_file_path, 'r') as file:
            sql_content = file.read()

        def extract_values(sql_content):
            insert_start = sql_content.find("INSERT INTO transactions VALUES")
            if insert_start == -1:
                raise ValueError("Aucune commande INSERT trouvée")
                
            values_start = sql_content.find("(", insert_start)
            values_end = sql_content.find(";", values_start)
            values_str = sql_content[values_start:values_end]
            
            rows = []
            value_lines = values_str.split('),')
            
            for line in value_lines:
                line = line.strip('()\n ')
                if line:
                    values = line.split(',')
                    transaction_id = int(values[0].strip())
                    amount = Decimal(values[1].strip())
                    customer_name = values[2].strip().strip("'")
                    rows.append((transaction_id, amount, customer_name))
                    
            return rows

        data = extract_values(sql_content)
        
        df = spark.createDataFrame(data, schema)
        
        os.makedirs(output_path, exist_ok=True)
        
        output_file = os.path.join(output_path, "transactions")
        df.write.mode("overwrite").parquet(output_file)
        
        print(f"✓ {df.count()} transactions ingérées avec succès")
        
        print("\nAperçu des données ingérées :")
        df.show()

    except Exception as e:
        print(f"✗ Erreur lors de l'ingestion SQL: {str(e)}")
        raise e