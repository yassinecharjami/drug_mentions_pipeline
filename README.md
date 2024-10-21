# drug_mentions_pipeline

This project is a data pipeline that processes CSV and JSON data containing information on drugs, pubmed articles, and clinical trials to generate a JSON file. The JSON file represents a graph of drug mentions in different journals based on the publications in pubmed and clinical trials. Also, it contains an SQL folder to answer sql questions. 

## Table of Contents

- [Technologies Used](#technologies-used)
- [Setup Instructions](#setup-instructions)
- [Running the Pipeline](#running-the-pipeline)
- [Testing](#testing)
- [Scaling](#scaling)

## Technologies Used

- **Python 3.10**: Core programming language for the pipeline.
- **Pandas**: For data manipulation and cleaning.
- **Docker**: For containerizing the pipeline.
- **Docker Compose**: To manage multi container Docker applications.
- **unittest**: Python's built-in testing framework.

## Setup Instructions

### Prerequisites
- **Docker** and **Docker compose** installed on the machine
- **Python 3.10** to run the pipeline alternatively on host machine

### Clone the repository

```bash
git clone git@github.com:yassinecharjami/drug_mentions_pipeline.git
cd drug_mentions_pipeline
```

### Using Docker

```bash
docker-compose build
```

### On local machine

Create virtual environment and install dependencies:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Running the Pipeline

### Using Docker

```bash
docker-compose up
```

### On local machine

```bash
python -m data_pipeline.pipeline
```

## Testing

### Using Docker

```bash
docker-compose run --rm pipeline python -m unittest discover tests
```

### On local machine

```bash
python -m unittest discover -s tests
```

## Scaling

To handle large files (terabytes) we can consider:
- Distributed Storage: like HDFS on on-premise or GCS (Google Cloud Storage) to store input/output dataframes.
- Distributed frameworks: like Apache Spark (using python, scala, java) or BigQuery (using SQL) to manipulate and clean data.
- File format: Convert CSV and JSON input files to Parquet for efficiency.