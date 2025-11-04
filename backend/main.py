from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import boto3
import json
from typing import List, Dict, Any
import asyncio
from datetime import datetime

app = FastAPI(title="Automation Dashboard API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# AWS Lambda client
lambda_client = boto3.client('lambda', region_name='us-east-1')

class TaskRequest(BaseModel):
    task_type: str
    parameters: Dict[str, Any]

class TaskResponse(BaseModel):
    task_id: str
    status: str
    result: Dict[str, Any] = None

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
    task_id = f"email_{datetime.now().timestamp()}"
    
    # Invoke Lambda function
    try:
        response = lambda_client.invoke(
            FunctionName='email-parser',
            InvocationType='RequestResponse',
            Payload=json.dumps(request.parameters)
        )
        
        result = json.loads(response['Payload'].read())
        
        task = TaskResponse(
            task_id=task_id,
            status="completed",
            result=result
        )
        
        tasks[task_id] = task.dict()
        return task
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/tasks/invoice-generate")
async def generate_invoice(request: TaskRequest):
    task_id = f"invoice_{datetime.now().timestamp()}"
    
    try:
        response = lambda_client.invoke(
            FunctionName='invoice-generator',
            InvocationType='RequestResponse',
            Payload=json.dumps(request.parameters)
        )
        
        result = json.loads(response['Payload'].read())
        
        task = TaskResponse(
            task_id=task_id,
            status="completed",
            result=result
        )
        
        tasks[task_id] = task.dict()
        return task
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/tasks/lead-score")
async def score_lead(request: TaskRequest):
    task_id = f"lead_{datetime.now().timestamp()}"
    
    try:
        response = lambda_client.invoke(
            FunctionName='lead-scorer',
            InvocationType='RequestResponse',
            Payload=json.dumps(request.parameters)
        )
        
        result = json.loads(response['Payload'].read())
        
        task = TaskResponse(
            task_id=task_id,
            status="completed",
            result=result
        )
        
        tasks[task_id] = task.dict()
        return task
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)