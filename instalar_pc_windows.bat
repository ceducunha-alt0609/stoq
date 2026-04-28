@echo off
setlocal
REM Instalador/atalho do Stoq PRO para Windows.
REM Se a URL do GitHub Pages mudar, altere a linha abaixo.
set APP_URL=https://ceducunha-alt0609.github.io/stoq/

echo Abrindo o Stoq PRO para instalacao como PWA...
echo.
echo Chrome: clique no icone de instalar na barra de endereco ou Menu ^> Salvar e compartilhar ^> Instalar pagina como app.
echo Edge: Menu ^> Aplicativos ^> Instalar este site como aplicativo.
echo.
start "" "%APP_URL%"
pause
