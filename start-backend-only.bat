@echo off
echo Starting Backend API Only...

cd backend
echo Starting FastAPI server on port 8000...
uvicorn main:app --reload --host 0.0.0.0 --port 8000

echo.
echo Backend API: http://localhost:8000
echo API Docs: http://localhost:8000/docs