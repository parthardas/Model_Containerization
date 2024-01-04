import os
import uuid
import logging
from io import StringIO

from fastapi import APIRouter, UploadFile
from fastapi.responses import JSONResponse
from models.datamodels import UserFeatureRequest, InsertUserResponse, \
InferenceRequest, InferenceResponse, InferencePostRequest
from utils.inference_model import KnnClassifier
from utils.services import insert_user, read_user, update_credit_score, fetch_credit_score, connect_to_database

model_path=os.getenv('MODEL_PATH')
scaler_path=os.getenv('SCALER_PATH')
le_path=os.getenv('LE_PATH')
model_key = os.getenv('MODEL_KEY')

model = KnnClassifier(None, model_path, scaler_path, le_path)
db_connection = connect_to_database()

logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S'
)

router = APIRouter()

@router.get("/ping", status_code=200)
async def healthcheck():
    """
    perform health check on api
    """
    return {"status": "OK"}

# we need to support two routes for train and inference 
@router.post("/add_user_details", response_model=InsertUserResponse)
async def add_user(user_feature_request: UserFeatureRequest):
    '''
    This is a post method to submit user for insertion in DB

    Returns success response with customer_id
    '''
    customer_id, error = insert_user(db_connection, 
        [user_feature_request.customer_id,
        user_feature_request.credit_history_age,
        user_feature_request.monthly_balance,
        user_feature_request.annual_income,
        user_feature_request.changed_credit_limit,
        user_feature_request.outstanding_debt, ])
    if customer_id:
        return InsertUserResponse(customer_id=customer_id)
    else:
        return JSONResponse(status_code=409, 
            content={"detail": f"customer with id: {user_feature_request.customer_id} already exists"})


@router.get("/get_credit_score", response_model=InferenceResponse)
async def update_user_feature(customer_id: str):
    '''
    This is a get method to fetch credit score for a given customer id

    Returns success response with credit score
    '''
    credit_score = fetch_credit_score(db_connection, customer_id, model_key)
    if credit_score:
        logging.info(f"fetch cached credit score for customer id: {customer_id} and model {model_key}: {credit_score}")
        return InferenceResponse(credit_score=credit_score)
    
    customer_details = read_user(db_connection, customer_id)
    if not customer_details:
        return JSONResponse(status_code=409, 
            content={"detail": f"customer with id: {customer_id} does not exist"})

    logging.info(f"get credit score for customer details: {customer_details}")
    credit_score = model.predict([customer_details[1:]])
    update_credit_score(db_connection, customer_id, model_key, credit_score[0])
    return InferenceResponse(credit_score=credit_score[0])
    

@router.post("/get_credit_score", response_model=InferenceResponse)
async def get_cached_score(inference_request: InferencePostRequest):
    '''
    This is a post method to get credit score with inserting the customer features

    Returns success response with credit score
    '''
    features = [inference_request.credit_history_age,
        inference_request.monthly_balance,
        inference_request.annual_income,
        inference_request.changed_credit_limit,
        inference_request.outstanding_debt, ]
    credit_score = model.predict([features])  
    return InferenceResponse(credit_score=credit_score[0])

@router.post("/train")
async def get_cached_score(csv_data: str):
    '''
    This is a post method to trigger the train job with the csv data 
    '''
    csv_string = StringIO(csv_data.file.read().decode('utf-8'))
    return {"status": "OK"} 