# VPN Watchdog - Автоматический мониторинг и восстановление VPN

## Два варианта установки

### 🖥️ Вариант 1: На локальном ПК (Windows)
Для мониторинга Hiddify на твоем компьютере

### 🌐 Вариант 2: На VPN сервере (Linux) - РЕКОМЕНДУЕТСЯ
Работает 24/7 независимо от твоего ПК

---

## 🌐 Установка на VPN сервер (Linux)

### Что делает:
✅ Работает 24/7 на сервере
✅ Проверяет VPN сервис каждые 60 секунд
✅ Автоматически перезапускает если упал
✅ Обновляет конфиги из GitHub каждые 2 часа
✅ Не зависит от твоего ПК

### Установка:

1. Скопируй файлы на сервер:
```bash
scp server_watchdog.sh vpn-watchdog.service install_server_watchdog.sh root@YOUR_SERVER_IP:/root/
```

2. Подключись к серверу:
```bash
ssh root@YOUR_SERVER_IP
```

3. Запусти установку:
```bash
chmod +x install_server_watchdog.sh
./install_server_watchdog.sh
```

### Управление:

Проверить статус:
```bash
systemctl status vpn-watchdog
```

Посмотреть логи:
```bash
journalctl -u vpn-watchdog -f
# или
tail -f /var/log/vpn_watchdog.log
```

Перезапустить:
```bash
systemctl restart vpn-watchdog
```

Остановить:
```bash
systemctl stop vpn-watchdog
```

---

## 🖥️ Установка на Windows (локальный ПК)

### Что делает:
✅ Проверяет работу интернета каждые 60 секунд
✅ Проверяет работу VPN (доступность заблокированных сайтов)
✅ Автоматически обновляет конфиги из GitHub
✅ Перезапускает Hiddify если VPN упал

### Установка:

1. Установи зависимости:
```bash
pip install -r requirements.txt
```

2. Отредактируй `vpn_watchdog.py` если нужно:
   - `HIDDIFY_PATH` - путь к Hiddify.exe
   - `CHECK_INTERVAL` - интервал проверки (секунды)

### Запуск:

Вручную:
```bash
python vpn_watchdog.py
```

Через bat файл:
Двойной клик на `start_watchdog.bat`

Автозапуск с Windows:
1. Win+R → `shell:startup`
2. Создай ярлык на `start_watchdog.bat`
3. Готово!

---

## Как это работает

1. Каждые 60 секунд проверяет интернет/VPN сервис
2. Если VPN не работает 2 раза подряд:
   - Обновляет конфиги из GitHub
   - Перезапускает VPN сервис
3. Каждые 2 часа обновляет конфиги автоматически
4. Все логи сохраняются для отладки
