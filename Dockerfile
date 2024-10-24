FROM python:3.10-slim

WORKDIR /drug_mentions_pipeline

COPY . .

RUN pip install -r requirements.txt

CMD ["python", "pipeline.py"]