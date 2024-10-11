# from fastapi import FastAPI, HTTPException
# from pydantic import BaseModel

# app = FastAPI()

# @app.get("/health")
# def principal():
#     return { "status": "ok"}


# class VectorItem(BaseModel):
#     nombre: str

# @app.post("/vector-search")
# def vector_search(item: VectorItem):
#     return { "nombre_recibido": item.nombre }

## TODO: descomentar

# import vertexai

# import vertexai.preview.generative_models as generative_models

PROJECT_ID = "docker-gcp-435814"  # @param {type:"string"}
LOCATION="us-central1"

from google.cloud import bigquery
from google.oauth2 import service_account

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

KEY_PATH="./docker-gcp-435814-d2739ae5e512.json"


credenciales = service_account.Credentials.from_service_account_file(KEY_PATH)

bq_client = bigquery.Client(credentials=credenciales, project=PROJECT_ID)

app = FastAPI()

class VectorItem(BaseModel):
    limite: int

@app.post("/vector-search")
def vector_search(item: VectorItem):

    QUERY_TEMPLATE = """
        SELECT distinct q.id, q.title
        FROM (SELECT * FROM `bigquery-public-data.stackoverflow.posts_questions`
        where Score > 0 ORDER BY View_Count desc) AS q
        LIMIT {limit} ;
        """
    query = QUERY_TEMPLATE.format(limit=item.limite)
    query_job = bq_client.query(query)
    rows = query_job.result()

    return { "resultados": [dict(row) for row in rows] }

