@echo off
SET "ROOT_DIR=%~dp0.."


setlocal
cd /d "%ROOT_DIR%"


REM upgrade pip install
pip install --upgrade pip setuptools

REM install project requirements
pip install --requirement requirements.txt
