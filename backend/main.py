from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import boto3
import json
from typing import List, Dict, Any, Optional
import asyncio
from datetime import datetime, timezone
import logging
import os
from mock_responses import mock_email_parse, mock_invoice_generate, mock_lead_score

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Automation Dashboard API")

# Secure CORS configuration
allowed_origins = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type", "Authorization"],
)

# AWS Lambda client with error handling (fallback to mock for demo)
try:
    lambda_client = boto3.client('lambda', region_name=os.getenv('AWS_REGION', 'us-east-1'))
except Exception as e:
    logger.warning(f"AWS Lambda client not available, using mock responses: {e}")
    lambda_client = None

class TaskRequest(BaseModel):
    task_type: str
    parameters: Dict[str, Any]

class TaskResponse(BaseModel):
    task_id: str
    status: str
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    timestamp: str

# In-memory task storage (use Redis/DynamoDB in production)
tasks = {}

@app.get("/")
async def root():
    return {"message": "Automation Dashboard API"}

@app.get("/tasks")
async def get_tasks():
    return {"tasks": list(tasks.values())}

@app.post("/tasks/email-parse")
async def parse_email(request: TaskRequest, background_tasks: BackgroundTasks):
    task_id = f"email_{datetime.now(timezone.utc).timestamp()}"
    
    try:
        logger.info(f"Processing email parse request: {task_id}")
        
        if lambda_client:
            response = lambda_client.invoke(
                FunctionName='email-parser',
                InvocationType='RequestResponse',
                Payload=json.dumps(request.parameters)
            )
            result = json.loads(response['Payload'].read())
        else:
            # Use mock response for demo
            result = {'body': mock_email_parse()}
        
        task = TaskResponse(
            task_id=task_id,
            status="completed",
            result=result,
            timestamp=datetime.now(timezone.utc).isoformat()
        )
        
        tasks[task_id] = task.dict()
        logger.info(f"Email parse completed: {task_id}")
        return task
        
    except Exception as e:
        logger.error(f"Email parse failed: {task_id}, error: {str(e)}")
        error_task = TaskResponse(
            task_id=task_id,
            status="failed",
            error=str(e),
            timestamp=datetime.now(timezone.utc).isoformat()
        )
        tasks[task_id] = error_task.dict()
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/tasks/invoice-generate")
async def generate_invoice(request: TaskRequest):
    task_id = f"invoice_{datetime.now(timezone.utc).timestamp()}"
    
    try:
        logger.info(f"Processing invoice generation: {task_id}")
        
        if lambda_client:
            response = lambda_client.invoke(
                FunctionName='invoice-generator',
                InvocationType='RequestResponse',
                Payload=json.dumps(request.parameters)
            )
            result = json.loads(response['Payload'].read())
        else:
            # Use mock response for demo
            result = {'body': mock_invoice_generate()}
        
        task = TaskResponse(
            task_id=task_id,
            status="completed",
            result=result,
            timestamp=datetime.now(timezone.utc).isoformat()
        )
        
        tasks[task_id] = task.dict()
        logger.info(f"Invoice generation completed: {task_id}")
        return task
        
    except Exception as e:
        logger.error(f"Invoice generation failed: {task_id}, error: {str(e)}")
        error_task = TaskResponse(
            task_id=task_id,
            status="failed",
            error=str(e),
            timestamp=datetime.now(timezone.utc).isoformat()
        )
        tasks[task_id] = error_task.dict()
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/tasks/lead-score")
async def score_lead(request: TaskRequest):
    task_id = f"lead_{datetime.now(timezone.utc).timestamp()}"
    
    try:
        logger.info(f"Processing lead scoring: {task_id}")
        
        if lambda_client:
            response = lambda_client.invoke(
                FunctionName='lead-scorer',
                InvocationType='RequestResponse',
                Payload=json.dumps(request.parameters)
            )
            result = json.loads(response['Payload'].read())
        else:
            # Use mock response for demo
            company_size = request.parameters.get('lead_data', {}).get('company_size', 1500)
            result = {'body': mock_lead_score(company_size)}
        
        task = TaskResponse(
            task_id=task_id,
            status="completed",
            result=result,
            timestamp=datetime.now(timezone.utc).isoformat()
        )
        
        tasks[task_id] = task.dict()
        logger.info(f"Lead scoring completed: {task_id}")
        return task
        
    except Exception as e:
        logger.error(f"Lead scoring failed: {task_id}, error: {str(e)}")
        error_task = TaskResponse(
            task_id=task_id,
            status="failed",
            error=str(e),
            timestamp=datetime.now(timezone.utc).isoformat()
        )
        tasks[task_id] = error_task.dict()
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)