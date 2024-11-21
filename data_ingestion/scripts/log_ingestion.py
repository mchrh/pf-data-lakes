from common import *
import re
from datetime import datetime

def parse_log_line(line):
    pattern = r'(\d+\.\d+\.\d+\.\d+) - - \[(.*?)\] "(.*?)" (\d+) (\d+) "(.*?)" "(.*?)"'
    match = re.match(pattern, line)
    
    if match:
        ip, timestamp, request, status, bytes, referer, user_agent = match.groups()
        
        method, path, protocol = request.split()
        
        timestamp = datetime.strptime(timestamp.split()[0], '%d/%b/%Y:%H:%M:%S')
        
        return {
            "ip": ip,
            "timestamp": timestamp,
            "method": method,
            "path": path,
            "protocol": protocol,
            "status": int(status),
            "bytes": int(bytes),
            "referer": referer,
            "user_agent": user_agent
        }
    return None

def ingest_logs(spark, input_path, output_path):
    try:
        log_schema = StructType([
            StructField("ip", StringType(), True),
            StructField("timestamp", TimestampType(), True),
            StructField("method", StringType(), True),
            StructField("path", StringType(), True),
            StructField("protocol", StringType(), True),
            StructField("status", IntegerType(), True),
            StructField("bytes", LongType(), True),
            StructField("referer", StringType(), True),
            StructField("user_agent", StringType(), True)
        ])

        with open(input_path, 'r') as file:
            log_data = [parse_log_line(line) for line in file if line.strip()]
        
        df = spark.createDataFrame([log for log in log_data if log], log_schema)
        
        df.write.mode("overwrite").parquet(output_path)
        print(f"✓ {df.count()} logs ingérés")

    except Exception as e:
        print(f"✗ Erreur lors de l'ingestion des logs: {str(e)}")
        raise e
