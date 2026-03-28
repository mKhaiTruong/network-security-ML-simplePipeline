import os, sys, pymongo, pandas as pd, certifi
ca = certifi.where()

from dotenv import load_dotenv
load_dotenv()

MONGO_DB_URL = os.getenv("MONGO_DB_URL")
print(MONGO_DB_URL)

from fastapi import FastAPI, File, UploadFile, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from uvicorn import run as app_run
from starlette.responses import RedirectResponse

from src.network_security.exception.exception import NetworkSecurityException
from src.network_security.logging.logger import logger
from src.network_security.pipeline.training_pipeline import TrainingPipeline
from src.network_security.utils.main_utils.utils import load_object
from src.network_security.utils.ml_utils.model.estimator import NetworkModel

from src.network_security.constants.training_pipeline import (
    DATA_INGESTION_DATABASE_NAME,
    DATA_INGESTION_COLLECTION_NAME
)

client = pymongo.MongoClient(MONGO_DB_URL, tlsCAFile=ca)
database = client[DATA_INGESTION_DATABASE_NAME]
collection = database[DATA_INGESTION_COLLECTION_NAME]

app = FastAPI()
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from fastapi.templating import Jinja2Templates
templates = Jinja2Templates(directory="./templates")

@app.get('/', tags=["authentication"])
async def index():
    return RedirectResponse(url="/docs")

@app.get('/train')
async def train_route():
    try: 
        train_pipeline = TrainingPipeline()
        train_pipeline.run_pipeline()
        return Response("Training successful !!")
    except Exception as e:
        raise NetworkSecurityException(e, sys)

@app.post("/predict")
async def predict_route(request: Request, file: UploadFile = File(...)):
    try:
        df = pd.read_csv(file.file)
        preprocessor = load_object("final_models/preprocessor.pkl")
        model = load_object("final_models/model.pkl")
        network_model = NetworkModel(preprocessor, model)
        
        y_pred = network_model.predict(x=df)
        df['predicted_column'] = y_pred
        
        df.to_csv("predicted_output/prediction.csv", index=False, header=True)
        table_html = df.to_html(classes='table table-striped')
        
        return templates.TemplateResponse("index.html", {
            "request": request,
            "table": table_html
        })
        
    except Exception as e:
        raise NetworkSecurityException(e, sys)
    
if __name__=='__main__':
    app_run(app, host="localhost", port=8000)