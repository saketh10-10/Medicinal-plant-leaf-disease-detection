@echo off
echo Starting Plant Disease Classification System...
echo.

echo Starting FastAPI Backend on port 8000...
start cmd /k "cd /d D:\PLANT\backend && python -m uvicorn main:app --reload --host 127.0.0.1 --port 8000"

timeout /t 3 /nobreak > nul

echo Starting React Frontend on port 5173...
start cmd /k "cd /d D:\PLANT\frontend && npm run dev"

echo.
echo Both servers are starting...
echo Backend: http://localhost:8000
echo Frontend: http://localhost:5173
echo API Docs: http://localhost:8000/docs
echo.
echo Press any key to exit...
pause > nul