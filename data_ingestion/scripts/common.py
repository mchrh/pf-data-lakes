from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, \
    TimestampType, DateType, DecimalType, LongType, ArrayType
import os

def create_spark_session():
    return SparkSession.builder \
        .appName("DataIngestion") \
        .getOrCreate()