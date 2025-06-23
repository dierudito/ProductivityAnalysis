@echo off
REM Batch file to run the full Python data science pipeline.

REM Change directory to the script's location.
REM The /d switch is important if the script is on a different drive than the default.
cd /d "C:\dev\Ds\ProductivityAnalysis"

REM Activate the Python virtual environment
echo Activating virtual environment...
call .\.venv\Scripts\activate.bat

REM Run the main Python pipeline script
echo Running Python pipeline...
python run_pipeline.py

echo Pipeline finished. Deactivating environment...
REM Deactivate the environment
call .\.venv\Scripts\deactivate.bat

REM The line below is for testing only. It keeps the window open.
REM Remove "pause" before scheduling the task.