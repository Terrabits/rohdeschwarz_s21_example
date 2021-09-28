@echo off
SET "ROOT_DIR=%~dp0.."


setlocal
cd /d "%ROOT_DIR%"


REM freeze requirements
pip freeze > requirements.txt.lock
