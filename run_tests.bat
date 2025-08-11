@echo off

echo === Ativando ambiente virtual ===
call venv\Script\activate

echo === Rodando testes e coverage ===
pytest --cov=. --cov-report=html

echo === Abrindo o relatorio HTML de cobertura ===
start htmlcov\index.html