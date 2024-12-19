import logging
import mysql.connector
from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col
from pyspark.sql.types import StructType, StructField, StringType


def create_spark_connection():
    try:
        s_conn = SparkSession.builder \
            .appName('SparkDataStreaming') \
            .config('spark.jars.packages', "org.apache.kafka:kafka-clients:3.9.0," 
                                           "org.apache.spark:spark-sql-kafka-0-10_2.12:3.4.1") \
            .getOrCreate()

        s_conn.sparkContext.setLogLevel("ERROR")
        logging.info("Spark connection created successfully!")
        return s_conn
    except Exception as e:
        logging.error(f"Couldn't create the spark session due to exception {e}")
        return None


def connect_to_kafka(spark_conn):
    try:
        spark_df = spark_conn.readStream \
            .format('kafka') \
            .option('kafka.bootstrap.servers', 'localhost:9092') \
            .option('subscribe', 'users_created') \
            .option('startingOffsets', 'earliest') \
            .option('fetch.max.bytes', '1048576') \
            .option('max.partition.fetch.bytes', '1048576') \
            .load()

        spark_df.printSchema()
        logging.info("Kafka DataFrame created successfully!")
        return spark_df
    except Exception as e:
        logging.warning(f"Kafka DataFrame could not be created: {e}")
        return None


def create_selection_df_from_kafka(spark_df):
    schema = StructType([
        StructField("id", StringType(), False),
        StructField("first_name", StringType(), False),
        StructField("last_name", StringType(), False),
        StructField("gender", StringType(), False),
        StructField("address", StringType(), False),
        StructField("post_code", StringType(), False),
        StructField("email", StringType(), False),
        StructField("username", StringType(), False),
        StructField("registered_date", StringType(), False),
        StructField("phone", StringType(), False),
        StructField("picture", StringType(), False)
    ])

    sel = spark_df.selectExpr("CAST(value AS STRING)") \
        .select(from_json(col('value'), schema).alias('data')).select("data.*")
    logging.info("DataFrame schema applied")
    return sel


import uuid

import uuid

def write_to_mysql(row):
    """Write a single row to MySQL."""
    connection = None
    cursor = None  # Ensure cursor is defined in the outer scope
    try:
        connection = mysql.connector.connect(
            host="localhost",
            port=3308,
            user="my_user",
            password="my_password",
            database="my_database"

        )

        cursor = connection.cursor()

        # Use a generated UUID if id is null
        row_id = row.id if row.id else str(uuid.uuid4())

        insert_query = """
        INSERT INTO created_users (id, first_name, last_name, gender, address, post_code, email, username, registered_date, phone, picture)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        data = (
            row_id,
            row.first_name,
            row.last_name,
            row.gender,
            row.address,
            row.post_code,
            row.email,
            row.username,
            row.registered_date,
            row.phone,
            row.picture
        )
        cursor.execute(insert_query, data)
        connection.commit()
        logging.info(f"Data inserted for {row.first_name} {row.last_name}")
    except mysql.connector.Error as e:
        logging.error(f"Error inserting data into MySQL: {e}")
    finally:
        # Close the cursor and connection only if they were successfully created
        if cursor is not None:
            cursor.close()
        if connection is not None:
            connection.close()




if __name__ == "__main__":
    spark_conn = create_spark_connection()

    if spark_conn is not None:
        spark_df = connect_to_kafka(spark_conn)

        if spark_df:
            selection_df = create_selection_df_from_kafka(spark_df)

            # Debug: Write to console to verify Kafka messages
            query = selection_df.writeStream \
                .format("console") \
                .outputMode("append") \
                .start()

            # Write to MySQL
            selection_df.writeStream \
                .foreach(write_to_mysql) \
                .outputMode("append") \
                .start() \
                .awaitTermination()

            query.awaitTermination()
