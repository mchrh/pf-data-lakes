from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *
import os
from decimal import Decimal
import sys

def create_spark_session():
    python_path = sys.executable
    
    return SparkSession.builder \
        .appName("DataLakeETL") \
        .config("spark.sql.warehouse.dir", "/data_lake/silver") \
        .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0") \
        .config("spark.python.worker.python", python_path) \
        .config("spark.pyspark.python", python_path) \
        .config("spark.pyspark.driver.python", python_path) \
        .getOrCreate()

def transform_transactions(spark, input_path, output_path):
    try:
        df = spark.read.parquet(input_path)
        
        transformed_df = df \
            .withColumn("processing_date", current_timestamp()) \
            .withColumn("is_high_value", when(col("amount") > 100, True).otherwise(False)) \
            .withColumn("amount_category", when(col("amount") < 50, "low")
                                         .when(col("amount") < 100, "medium")
                                         .otherwise("high"))

        transformed_df.write.mode("overwrite").parquet(output_path)
        
        print(f"✓ Transformation des transactions réussie: {transformed_df.count()} lignes traitées")
        print("\nAperçu des données transformées:")
        transformed_df.show()

    except Exception as e:
        print(f"✗ Erreur lors de la transformation des transactions: {str(e)}")
        raise e

def transform_logs(spark, input_path, output_path):
    try:
        df = spark.read.parquet(input_path)
        
        transformed_df = df \
            .withColumn("processing_timestamp", current_timestamp()) \
            .withColumn("is_error", col("status") >= 400) \
            .withColumn("is_mobile", expr("user_agent like '%Mobile%'"))
            
        hourly_metrics = transformed_df \
            .groupBy(
                hour("timestamp").alias("hour"),
                col("method"),
                col("is_error")
            ) \
            .agg(
                count("*").alias("request_count"),
                sum("bytes").alias("total_bytes"),
                countDistinct("ip").alias("unique_visitors")
            )

        os.makedirs(output_path, exist_ok=True)
        hourly_metrics.write.mode("overwrite").parquet(output_path)
        
        print(f"✓ Transformation des logs réussie")
        print("\nAperçu des métriques horaires:")
        hourly_metrics.show()

    except Exception as e:
        print(f"✗ Erreur lors de la transformation des logs: {str(e)}")
        raise e

def transform_social_media(spark, input_path, output_path):
    try:
        df = spark.read.parquet(input_path)
        
        transformed_df = df \
            .withColumn("processing_date", current_timestamp()) \
            .withColumn("content_length", length(col("content"))) \
            .withColumn("hashtag_count", size("tags"))
            
        os.makedirs(output_path, exist_ok=True)
        transformed_df.write.mode("overwrite").parquet(output_path)
        
        print(f"✓ Transformation des données sociales réussie: {transformed_df.count()} posts traités")
        print("\nAperçu des données transformées:")
        transformed_df.show()

    except Exception as e:
        print(f"✗ Erreur lors de la transformation des données sociales: {str(e)}")
        raise e

def transform_ad_clicks_stream(spark, input_path, output_path):
    try:
        print("\nDémarrage de la transformation du stream de clics publicitaires...")
        
        os.makedirs(output_path, exist_ok=True)
        checkpoint_path = os.path.join(output_path, "checkpoints")
        
        input_schema = StructType([
            StructField("click_id", StringType(), True),
            StructField("ad_id", StringType(), True),
            StructField("user_id", StringType(), True),
            StructField("timestamp", StringType(), True),
            StructField("page_url", StringType(), True),
            StructField("campaign_id", StringType(), True),
            StructField("cost_per_click", StringType(), True),
            StructField("ingestion_timestamp", TimestampType(), True)
        ])
        
        df = spark.readStream \
            .schema(input_schema) \
            .format("parquet") \
            .load(input_path)
        
        converted_df = df \
            .withColumn("timestamp", to_timestamp(col("timestamp"))) \
            .withColumn("cost_per_click", col("cost_per_click").cast(DecimalType(10, 2)))
        
        transformed_df = converted_df \
            .withColumn("processing_timestamp", current_timestamp()) \
            .withColumn("hour_of_day", hour(col("timestamp"))) \
            .withColumn("cost_category", 
                       when(col("cost_per_click") < 0.3, "low")
                       .when(col("cost_per_click") < 0.7, "medium")
                       .otherwise("high"))
        
        windowed_df = transformed_df \
            .withWatermark("timestamp", "1 hour")
        
        aggregated_df = windowed_df \
            .groupBy(
                window(col("timestamp"), "1 hour"),
                col("campaign_id"),
                col("cost_category")
            ) \
            .agg(
                count("*").alias("click_count"),
                sum("cost_per_click").alias("total_cost"),
                avg("cost_per_click").alias("avg_cost"),
                approx_count_distinct("user_id").alias("unique_users")  
            )

        query = aggregated_df \
            .writeStream \
            .outputMode("append") \
            .format("parquet") \
            .option("path", output_path) \
            .option("checkpointLocation", checkpoint_path) \
            .trigger(processingTime="10 seconds") \
            .start()
        
        print("✓ Transformation du stream démarrée")
        print("\nSchéma des données transformées :")
        aggregated_df.printSchema()
        print("\nPour arrêter, appuyez sur Ctrl+C")
        
        query.awaitTermination()

    except Exception as e:
        print(f"✗ Erreur lors de la transformation du stream: {str(e)}")
        raise e
    
def main():
    spark = create_spark_session()
    
    try:
        raw_base = "../../data_lake/raw"
        silver_base = "../../data_lake/silver"
        
        print("\n=== Transformation des données batch ===")
        
        print("\nTransformation des transactions...")
        transform_transactions(
            spark,
            os.path.join(raw_base, "sql_data/transactions"),
            os.path.join(silver_base, "transactions")
        )
        
        print("\nTransformation des logs...")
        transform_logs(
            spark,
            os.path.join(raw_base, "web_logs"),
            os.path.join(silver_base, "web_logs")
        )
        
        print("\nTransformation des données sociales...")
        transform_social_media(
            spark,
            os.path.join(raw_base, "social_media"),
            os.path.join(silver_base, "social_media")
        )
        
        print("\n=== Transformation du stream de clics ===")
        transform_ad_clicks_stream(
            spark,
            os.path.join(raw_base, "ad_clicks"),
            os.path.join(silver_base, "ad_clicks")
        )
        
    except KeyboardInterrupt:
        print("\nArrêt demandé par l'utilisateur...")
    except Exception as e:
        print(f"\n✗ Erreur lors des transformations: {str(e)}")
        raise e
    finally:
        spark.stop()

if __name__ == "__main__":
    main()