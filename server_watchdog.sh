#!/bin/bash

# VPN Server Watchdog - работает на сервере 24/7
# Мониторит VPN сервер и автоматически чинит если что-то упало

SUBSCRIPTION_URL="https://raw.githubusercontent.com/modrinthmodification-create/ownedvpn/main/subscription.txt"
CHECK_INTERVAL=60
LOG_FILE="/var/log/vpn_watchdog.log"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

check_internet() {
    if ping -c 1 8.8.8.8 &> /dev/null; then
        return 0
    else
        return 1
    fi
}

check_vpn_service() {
    # Проверяем работает ли Xray/V2Ray
    if systemctl is-active --quiet xray; then
        return 0
    elif systemctl is-active --quiet v2ray; then
        return 0
    else
        return 1
    fi
}

update_configs() {
    log "Обновление конфигов из GitHub..."

    # Скачиваем свежие конфиги
    if curl -s "$SUBSCRIPTION_URL" -o /tmp/subscription.txt; then
        log "✓ Конфиги успешно обновлены"
        return 0
    else
        log "✗ Ошибка загрузки конфигов"
        return 1
    fi
}

restart_vpn() {
    log "Перезапуск VPN сервиса..."

    if systemctl is-active --quiet xray; then
        systemctl restart xray
        log "✓ Xray перезапущен"
    elif systemctl is-active --quiet v2ray; then
        systemctl restart v2ray
        log "✓ V2Ray перезапущен"
    fi

    sleep 5
}

main() {
    log "🚀 VPN Server Watchdog запущен"

    consecutive_failures=0
    last_update=0

    while true; do
        # Проверка интернета
        if ! check_internet; then
            log "⚠ Нет интернета на сервере!"
            ((consecutive_failures++))

            if [ $consecutive_failures -ge 3 ]; then
                log "🔄 Попытка восстановления..."
                restart_vpn
                consecutive_failures=0
                sleep 30
            fi

            sleep $CHECK_INTERVAL
            continue
        fi

        # Проверка VPN сервиса
        if check_vpn_service; then
            log "✓ VPN работает нормально"
            consecutive_failures=0
        else
            log "⚠ VPN сервис не работает!"
            ((consecutive_failures++))

            if [ $consecutive_failures -ge 2 ]; then
                log "🔄 Автоматическое восстановление..."
                update_configs
                restart_vpn
                consecutive_failures=0
                sleep 30
            fi
        fi

        # Обновление конфигов каждые 2 часа
        current_time=$(date +%s)
        if [ $((current_time - last_update)) -gt 7200 ]; then
            log "🔄 Плановое обновление конфигов..."
            update_configs
            last_update=$current_time
        fi

        sleep $CHECK_INTERVAL
    done
}

main
