# Real-Time Data Pipeline with Kafka, Spark, Cassandra, and SQL

This project demonstrates a real-time data pipeline where data is generated using the Random User API, ingested into Kafka using Apache Airflow, processed with Apache Spark, and stored in Cassandra and MySQL databases for further analytics. The entire architecture runs on Dockerized services.

## Table of Contents
1. [System Architecture](#system-architecture)
2. [Technologies Used](#technologies-used)
3. [Workflow](#workflow)
4. [Setup Instructions](#setup-instructions)
5. [Project Components](#project-components)
6. [Running the Pipeline](#running-the-pipeline)
7. [Future Enhancements](#future-enhancements)
8. [Conclusion](#conclusion)

---

## System Architecture

![System Architecture](./system_architecture.png)

The system architecture includes:
- **Random User API**: Generates random user data.
- **Airflow**: Orchestrates data ingestion and pushes it to Kafka.
- **Kafka**: Acts as a messaging system for real-time data streaming.
- **Zookeeper**: Coordinates Kafka brokers.
- **Spark (Master/Workers)**: Processes data from Kafka streams.
- **Cassandra**: Stores processed data for scalable NoSQL querying.
- **PostgreSQL**: Stores structured data for analytical querying.
- **Control Center & Schema Registry**: Monitor Kafka topics and manage schemas.

---

## Technologies Used

- **Random User API**: [API Documentation](https://randomuser.me/)
- **Apache Airflow**: Workflow orchestration.
- **Apache Kafka**: Distributed streaming platform.
- **Apache Spark**: Distributed data processing.
- **Cassandra**: NoSQL database for high-throughput storage.
- **PostgreSQL**: Relational database for structured data.
- **Docker**: Containerization for all components.

---

## Workflow

1. **Data Generation**:
   - Data is fetched from the Random User API using Apache Airflow.

2. **Kafka Streaming**:
   - Airflow pushes the generated data into a Kafka topic (`users_created`).

3. **Data Processing**:
   - Spark (Master-Worker architecture) processes the data from the Kafka topic.

4. **Data Storage**:
   - Processed data is stored in both:
     - **Cassandra** for scalable and fast NoSQL queries.
     - **PostgreSQL** for structured relational queries.

---

## Setup Instructions

### Prerequisites

1. Install **Docker** and **Docker Compose** on your system.
2. Clone this repository:
   ```bash
   git clone <your-repository-url>
   cd <repository-directory>
Install Python 3.9 and set up a virtual environment:
bash
Copy code
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
Starting the Dockerized Services
Build and start all services:
bash
Copy code
docker-compose up -d
Verify that all services are running:
bash
Copy code
docker ps
Ensure zookeeper, broker, schema-registry, control-center, airflow, postgres, mysql, spark-master, spark-worker, and cassandra containers are up and running.
Configuring Apache Airflow
Access the Airflow Web UI:

arduino
Copy code
http://localhost:8080
Login credentials:

Username: airflow
Password: airflow
Upload the DAG (random_user_to_kafka.py) into the dags/ folder:

bash
Copy code
cp random_user_to_kafka.py ./dags
Trigger the DAG from the Airflow UI to start fetching data from the Random User API.

Setting Up Kafka
Access the Kafka Control Center:
arduino
Copy code
http://localhost:9021
Verify that the topic users_created has been created.
Monitor the data being published to the topic.
Configuring Apache Spark
Ensure the Spark Master and Worker services are running:

Spark Master: http://localhost:9090
The Spark job (kafka_to_spark_to_cassandra.py) will process the data stream.

Deploy the Spark script:

bash
Copy code
spark-submit --master spark://spark-master:7077 kafka_to_spark_to_cassandra.py
Accessing Stored Data
Cassandra:

Connect to the Cassandra container:
bash
Copy code
docker exec -it cassandra cqlsh
Query the stored data:
sql
Copy code
SELECT * FROM user_data;
PostgreSQL:

Connect to the PostgreSQL database:
bash
Copy code
docker exec -it postgres psql -U airflow -d airflow
Query the stored data:
sql
Copy code
SELECT * FROM user_data;
Project Components
Random User API Script:

Fetches random user data in JSON format.
Used in Airflow DAG.
Kafka Producer:

Pushes the generated user data to the Kafka topic.
Spark Streaming Job:

Reads data from Kafka, processes it, and writes it to Cassandra and PostgreSQL.
Cassandra Schema:

Defines the schema for storing user data.
PostgreSQL Schema:

Defines the schema for storing relational data.
Running the Pipeline
Start the services using Docker Compose.
Trigger the Airflow DAG to generate data.
Monitor Kafka for incoming data.
Deploy the Spark streaming job to process the data.
Query the data in Cassandra and PostgreSQL.
Future Enhancements
Add real-time dashboards using Grafana for monitoring data pipelines.
Include a data validation layer for cleaning incoming data.
Implement machine learning models for real-time analytics.
Use Avro or Protobuf for efficient serialization.
Conclusion
This project demonstrates a robust real-time data pipeline for ingesting, processing, and storing data using modern big data tools like Kafka, Spark, Cassandra, and SQL databases. The modular and scalable architecture ensures extensibility for future needs.

Author
Chaitanya Inamdar
inamdar.chaitanya6398@gmail.com






