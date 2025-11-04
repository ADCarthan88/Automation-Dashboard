@echo off
echo Starting Automation Dashboard Demo...

echo.
echo [1/3] Starting Backend API...
cd backend
start "Backend API" cmd /k "uvicorn main:app --reload --host 0.0.0.0 --port 8000"

echo.
echo [2/3] Waiting for backend to start...
timeout /t 5 /nobreak > nul

echo.
echo [3/3] Starting Frontend...
cd ..\frontend
start "Frontend" cmd /k "npm start"

echo.
echo ========================================
echo   AUTOMATION DASHBOARD DEMO READY!
echo ========================================
echo.
echo Frontend: http://localhost:3000
echo Backend API: http://localhost:8000
echo API Docs: http://localhost:8000/docs
echo.
echo Press any key to open browser...
pause > nul

start http://localhost:3000
start http://localhost:8000/docs