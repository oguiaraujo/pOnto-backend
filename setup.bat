@echo off
echo ================================
echo        Configurando pOnto
echo ================================

python --version >nul 2>&1
if errorlevel 1 (
    echo ERRO: Python nao encontrado.
    echo Instale em https://www.python.org/downloads/
    pause
    exit
)

echo Criando ambiente virtual...
python -m venv .venv

echo Instalando dependencias...
.venv\Scripts\pip install -r requirements.txt

echo Criando arquivo .env...
.venv\Scripts\python setup_env.py

echo Rodando migracoes...
.venv\Scripts\python manage.py makemigrations
.venv\Scripts\python manage.py migrate

echo.
.venv\Scripts\python manage.py createsuperuser

echo.
echo ================================
echo  Configuracao concluida!
echo  Execute o iniciar.bat para usar
echo ================================
pause