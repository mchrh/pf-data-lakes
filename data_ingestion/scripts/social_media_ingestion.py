from common import *
from pyspark.sql.functions import explode
import json

def ingest_social_media(spark, input_path, output_path):
    try:
        with open(input_path, 'r') as file:
            json_data = json.load(file)
        
        posts_data = json_data['posts']
        
        post_schema = StructType([
            StructField("post_id", StringType(), False),
            StructField("user_id", StringType(), True),
            StructField("content", StringType(), True),
            StructField("timestamp", StringType(), True),
            StructField("likes", IntegerType(), True),
            StructField("tags", ArrayType(StringType()), True),
            StructField("platform", StringType(), True)
        ])
        
        df = spark.createDataFrame(posts_data, schema=post_schema)
        
        os.makedirs(output_path, exist_ok=True)
        
        df.write.mode("overwrite").parquet(output_path)
        
        print(f"✓ {df.count()} posts sociaux ingérés")
        
        print("\nAperçu des données ingérées :")
        df.show(truncate=False)

    except Exception as e:
        print(f"✗ Erreur lors de l'ingestion des médias sociaux: {str(e)}")
        raise e