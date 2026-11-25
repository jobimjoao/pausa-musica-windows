@echo off
echo Instalando dependencias...
python -m pip install --upgrade winrt-runtime winrt-Windows.Media.Control winrt-Windows.Foundation winrt-Windows.Foundation.Collections
echo.
echo Pronto. Teste com:  python pausa_musica.py --listar
pause
