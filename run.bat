@echo off
REM Quick Start Script for Windows

echo ====================================
echo Company Review Platform - Quick Start
echo ====================================

REM Check if virtual environment exists
if not exist "venv\" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt --quiet

REM Run the application
echo.
echo ====================================
echo Starting the application...
echo ====================================
echo.
echo Access the application at: http://127.0.0.1:5000
echo.
echo Press Ctrl+C to stop the server
echo.

python app.py

pause
