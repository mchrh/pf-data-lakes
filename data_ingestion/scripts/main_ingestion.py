from common import *
import os
import sys


def main():
    os.environ['PYSPARK_PYTHON'] = sys.executable
    os.environ['PYSPARK_DRIVER_PYTHON'] = sys.executable
    spark = create_spark_session()

    try:
        input_base = "data_ingestion/sample_data"
        output_base = "data_lake/raw"

        os.makedirs(output_base, exist_ok=True)

        from sql_ingestion import ingest_sql_data
        from social_media_ingestion import ingest_social_media
        from log_ingestion import ingest_logs

        sql_path = os.path.join(input_base, "transactions.sql")
        sql_output = os.path.join(output_base, "sql_data")
        ingest_sql_data(spark, sql_path, sql_output)

        social_path = os.path.join(input_base, "social_media_posts.json")
        social_output = os.path.join(output_base, "social_media")
        ingest_social_media(spark, social_path, social_output)

        logs_path = os.path.join(input_base, "web_server.log")
        logs_output = os.path.join(output_base, "web_logs")
        ingest_logs(spark, logs_path, logs_output)

        print("✓ Ingestion batch terminée avec succès")

    except Exception as e:
        print(f"✗ Erreur lors de l'ingestion: {str(e)}")
        raise e
    finally:
        spark.stop()

if __name__ == "__main__":
    main()