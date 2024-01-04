from re import L
from typing import List
from typing import Optional
from pydantic import BaseModel, validator

class UserFeatureRequest(BaseModel):
    """This is the model for insert user api request"""
    customer_id: str
    credit_history_age: float
    monthly_balance: float
    annual_income: float
    changed_credit_limit: float
    outstanding_debt: float

class InsertUserResponse(BaseModel):
    """This is the model for insert user api response"""
    customer_id: str

class InferenceResponse(BaseModel):
    """This is the model for inference api request"""
    credit_score: float | str

class InferenceRequest(BaseModel):
    """This is the model for inference api response"""
    customer_id: str
    @validator("customer_id")
    def check_customer_id(cls, value):
        assert value != '', f"{value} cannot be empty string"
        return value

class InferencePostRequest(BaseModel):
    """This is the model for insert user api request without registering the user"""
    credit_history_age: float
    monthly_balance: float
    annual_income: float
    changed_credit_limit: float
    outstanding_debt: float