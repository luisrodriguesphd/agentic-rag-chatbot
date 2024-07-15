@echo off


set REPO_NAME=agentic-rag-chatbot
echo Start setting up the %REPO_NAME% repository


echo ****************************************
echo Install pip using ensurepip and upgrade
echo ****************************************
python -m ensurepip --upgrade
python -m pip install --upgrade pip
if "%errorlevel%" neq 0 (
    echo Failed to ensure the installation of pip for Python
)


echo ****************************************
echo Create and Activate Virtual Environment
echo ****************************************
call python -m venv venv 
call .\venv\Scripts\activate
if "%errorlevel%" neq 0 (
    echo Failed to create and activate virtual environment
)


echo ****************************************
echo Install Requirements
echo ****************************************
python -m pip install --upgrade pip
pip install -r requirements_dev.in
pip install -r requirements.in
pip install -e .
if "%errorlevel%" neq 0 (
    echo Failed to install requirements for development
)


echo ****************************************
echo Finish setting up the %REPO_NAME% repository
echo ****************************************
