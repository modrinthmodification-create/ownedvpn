#!/bin/bash

# Скрипт установки VPN Watchdog на сервер
# Запускать на сервере от root

set -e

echo "🚀 Установка VPN Server Watchdog..."

# Копируем скрипт
cp server_watchdog.sh /root/server_watchdog.sh
chmod +x /root/server_watchdog.sh

# Устанавливаем systemd сервис
cp vpn-watchdog.service /etc/systemd/system/vpn-watchdog.service

# Перезагружаем systemd
systemctl daemon-reload

# Включаем автозапуск
systemctl enable vpn-watchdog

# Запускаем сервис
systemctl start vpn-watchdog

echo ""
echo "✅ VPN Watchdog успешно установлен!"
echo ""
echo "Полезные команды:"
echo "  systemctl status vpn-watchdog   - статус"
echo "  systemctl restart vpn-watchdog  - перезапуск"
echo "  journalctl -u vpn-watchdog -f   - логи в реальном времени"
echo "  tail -f /var/log/vpn_watchdog.log - логи watchdog"
