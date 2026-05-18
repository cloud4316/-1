# Скрипт для запуска Django сервера в локальной сети
Write-Host "========================================" -ForegroundColor Green
Write-Host "   Запуск Django сервера в локальной сети" -ForegroundColor Green  
Write-Host "========================================" -ForegroundColor Green
Write-Host ""

# Получаем IP адрес компьютера
$networkAdapters = Get-NetIPAddress -AddressFamily IPv4 | Where-Object { $_.IPAddress -notlike "127.*" -and $_.IPAddress -notlike "169.*" }
$localIP = $networkAdapters | Select-Object -First 1 | Select-Object -ExpandProperty IPAddress

if ($localIP) {
    Write-Host "Ваш IP адрес: $localIP" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Сервер будет доступен по адресам:" -ForegroundColor Cyan
    Write-Host "  - Локально: http://127.0.0.1:8000" -ForegroundColor White
    Write-Host "  - В сети:   http://$localIP:8000" -ForegroundColor White
    Write-Host ""
    
    # Проверяем, что мы в правильной директории
    if (Test-Path "manage.py") {
        Write-Host "========================================" -ForegroundColor Green
        Write-Host "Для остановки сервера нажмите Ctrl+C" -ForegroundColor Red
        Write-Host "========================================" -ForegroundColor Green
        Write-Host ""
        
        # Запускаем Django сервер
        python manage.py runserver 0.0.0.0:8000
    } else {
        Write-Host "ОШИБКА: Файл manage.py не найден!" -ForegroundColor Red
        Write-Host "Убедитесь, что вы находитесь в корневой директории Django проекта." -ForegroundColor Red
    }
} else {
    Write-Host "ОШИБКА: Не удалось определить IP адрес!" -ForegroundColor Red
    Write-Host "Запускаем сервер только локально..." -ForegroundColor Yellow
    python manage.py runserver 127.0.0.1:8000
}

Write-Host ""
Write-Host "Нажмите любую клавишу для выхода..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")