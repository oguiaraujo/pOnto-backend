@echo off
echo ================================
echo        Configurando pOnto
echo ================================

:: Verifica se o Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo ERRO: Python nao encontrado.
    echo Instale em https://www.python.org/downloads/
    pause
    exit
)

echo Criando ambiente virtual...
python -m venv .venv

:: Ativa o ambiente virtual
call .venv\Scripts\activate

echo Instalando dependencias...
pip install -r requirements.txt

echo Criando arquivo .env...
python setup_env.py

echo Rodando migracoes...
python manage.py makemigrations
python manage.py migrate

:: Cria superusuário
echo.
python manage.py createsuperuser

echo.
echo ================================
echo  Configuracao concluida!
echo  Execute o iniciar.bat para usar
echo ================================
pause