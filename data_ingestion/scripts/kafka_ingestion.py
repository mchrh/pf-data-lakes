from common import *
from kafka import KafkaProducer, KafkaConsumer
import json
from datetime import datetime
import time
from pyspark.sql.functions import from_json, col, current_timestamp

def create_spark_session_with_kafka():
    import sys
    python_path = sys.executable
    
    return SparkSession.builder \
        .appName("KafkaIngestion") \
        .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0") \
        .config("spark.python.worker.python", python_path) \
        .config("spark.pyspark.python", python_path) \
        .config("spark.pyspark.driver.python", python_path) \
        .config("spark.sql.streaming.checkpointLocation", "/tmp/checkpoint") \
        .getOrCreate()

class AdClicksKafkaIngestor:
    def __init__(self, kafka_bootstrap_servers=['localhost:9092']):
        self._wait_for_kafka(kafka_bootstrap_servers)
        
        self.producer = KafkaProducer(
            bootstrap_servers=kafka_bootstrap_servers,
            value_serializer=lambda x: json.dumps(x).encode('utf-8'),
            api_version=(2, 5, 0)
        )
        
        self.consumer = KafkaConsumer(
            'ad_clicks',
            bootstrap_servers=kafka_bootstrap_servers,
            auto_offset_reset='latest',
            enable_auto_commit=True,
            group_id='ad_clicks_consumer_group',
            value_deserializer=lambda x: json.loads(x.decode('utf-8')),
            api_version=(2, 5, 0)
        )
        
        self.spark = create_spark_session_with_kafka()

    def _wait_for_kafka(self, bootstrap_servers, max_retries=5, retry_delay=5):
        print("Tentative de connexion à Kafka...")
        retries = 0
        while retries < max_retries:
            try:
                producer = KafkaProducer(
                    bootstrap_servers=bootstrap_servers,
                    api_version=(2, 5, 0)
                )
                producer.close()
                print("✓ Connexion à Kafka établie")
                return
            except Exception as e:
                retries += 1
                if retries < max_retries:
                    print(f"Tentative {retries}/{max_retries} échouée. Nouvelle tentative dans {retry_delay} secondes...")
                    time.sleep(retry_delay)
                else:
                    raise Exception("Impossible de se connecter à Kafka après plusieurs tentatives")

    def produce_sample_data(self, sample_file_path):
        try:
            print(f"Lecture du fichier {sample_file_path}...")
            with open(sample_file_path, 'r') as file:
                data = json.load(file)
                
            print("Envoi des données vers Kafka...")
            self.producer.send('ad_clicks', value=data)
            self.producer.flush()
            print("✓ Données envoyées au topic Kafka")
            
            print("\nDonnées envoyées:")
            print(json.dumps(data, indent=2))
            
        except FileNotFoundError:
            print(f"✗ Fichier non trouvé: {sample_file_path}")
        except json.JSONDecodeError:
            print("✗ Erreur de parsing JSON")
        except Exception as e:
            print(f"✗ Erreur lors de l'envoi des données à Kafka: {str(e)}")

    def process_message(self, message):
        try:
            message['ingestion_timestamp'] = datetime.now().isoformat()
            return message
        except Exception as e:
            print(f"✗ Erreur de traitement du message: {str(e)}")
            return None



    def ingest_stream(self, output_path):
        try:
            print("Démarrage de l'ingestion en temps réel...")
            
            os.makedirs(output_path, exist_ok=True)
            
            click_schema = StructType([
                StructField("click_id", StringType(), True),
                StructField("ad_id", StringType(), True),
                StructField("user_id", StringType(), True),
                StructField("timestamp", StringType(), True),
                StructField("page_url", StringType(), True),
                StructField("campaign_id", StringType(), True),
                StructField("cost_per_click", StringType(), True)
            ])

            df = self.spark \
                .readStream \
                .format("kafka") \
                .option("kafka.bootstrap.servers", "localhost:9092") \
                .option("subscribe", "ad_clicks") \
                .option("startingOffsets", "earliest") \
                .load()

            parsed_df = df.selectExpr("CAST(value AS STRING)") \
                .select(from_json(col("value"), click_schema).alias("data")) \
                .select("data.*") \
                .withColumn("ingestion_timestamp", current_timestamp())

            print("\nSchéma du DataFrame:")
            parsed_df.printSchema()

            checkpoint_path = os.path.join(output_path, "checkpoints")
            print(f"\nUtilisation du checkpoint path: {checkpoint_path}")
            
            query = parsed_df \
                .writeStream \
                .outputMode("append") \
                .format("parquet") \
                .option("path", output_path) \
                .option("checkpointLocation", checkpoint_path) \
                .trigger(processingTime="5 seconds") \
                .start()

            print("\n✓ Stream démarré. En attente de données...")
            print("Pour arrêter, appuyez sur Ctrl+C")
            
            query.awaitTermination()

        except Exception as e:
            print(f"✗ Erreur lors de l'ingestion streaming: {str(e)}")
            raise e

    def stop(self):
        try:
            if hasattr(self, 'producer'):
                self.producer.close()
            if hasattr(self, 'consumer'):
                self.consumer.close()
            if hasattr(self, 'spark'):
                self.spark.stop()
            print("✓ Arrêt propre effectué")
        except Exception as e:
            print(f"✗ Erreur lors de l'arrêt: {str(e)}")

if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    sample_data_path = os.path.join(base_dir, "data_ingestion", "sample_data", "ad_clicks.json")
    output_path = os.path.join(base_dir, "data_lake", "raw", "ad_clicks")

    ingestor = None
    try:
        ingestor = AdClicksKafkaIngestor()
        os.makedirs(output_path, exist_ok=True)
        ingestor.produce_sample_data(sample_data_path)
        ingestor.ingest_stream(output_path)

    except KeyboardInterrupt:
        print("\nArrêt demandé par l'utilisateur...")
    except Exception as e:
        print(f"\n✗ Erreur : {str(e)}")
    finally:
        if ingestor:
            ingestor.stop()