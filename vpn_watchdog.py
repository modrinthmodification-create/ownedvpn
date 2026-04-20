import time
import subprocess
import requests
import os
import sys
from datetime import datetime

# Фикс кодировки для Windows
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

# Конфигурация
SUBSCRIPTION_URL = "https://raw.githubusercontent.com/modrinthmodification-create/ownedvpn/main/subscription.txt"
LOCAL_SUBSCRIPTION = r"C:\scripts\vpn-subscription\subscription.txt"
CHECK_INTERVAL = 60  # Проверка каждые 60 секунд
HIDDIFY_PATH = r"C:\Program Files\Hiddify\Hiddify.exe"  # Путь к Hiddify

def log(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        print(f"[{timestamp}] {message}")
    except UnicodeEncodeError:
        # Fallback без эмодзи
        clean_msg = message.encode('ascii', 'ignore').decode('ascii')
        print(f"[{timestamp}] {clean_msg}")

def check_internet():
    """Проверка доступности интернета"""
    try:
        requests.get("https://www.google.com", timeout=5)
        return True
    except:
        return False

def check_vpn_connection():
    """Проверка работы VPN через доступность заблокированных сайтов"""
    blocked_sites = [
        "https://twitter.com",
        "https://facebook.com",
        "https://instagram.com"
    ]

    for site in blocked_sites:
        try:
            response = requests.get(site, timeout=5)
            if response.status_code == 200:
                return True
        except:
            continue

    return False

def update_subscription():
    """Обновление subscription файла из GitHub"""
    try:
        log("Обновление конфигов из GitHub...")
        response = requests.get(SUBSCRIPTION_URL, timeout=10)

        if response.status_code == 200:
            with open(LOCAL_SUBSCRIPTION, 'w', encoding='utf-8') as f:
                f.write(response.text)
            log("✅ Конфиги успешно обновлены")
            return True
        else:
            log(f"❌ Ошибка загрузки: HTTP {response.status_code}")
            return False
    except Exception as e:
        log(f"❌ Ошибка обновления: {e}")
        return False

def restart_hiddify():
    """Перезапуск Hiddify"""
    try:
        log("Перезапуск Hiddify...")

        # Закрываем Hiddify
        subprocess.run(["taskkill", "/F", "/IM", "Hiddify.exe"],
                      capture_output=True, timeout=5)
        time.sleep(2)

        # Запускаем Hiddify
        if os.path.exists(HIDDIFY_PATH):
            subprocess.Popen([HIDDIFY_PATH], shell=True)
            log("✅ Hiddify перезапущен")
            return True
        else:
            log(f"❌ Hiddify не найден: {HIDDIFY_PATH}")
            return False
    except Exception as e:
        log(f"❌ Ошибка перезапуска: {e}")
        return False

def main():
    log("🚀 VPN Watchdog запущен")
    log(f"Проверка каждые {CHECK_INTERVAL} секунд")

    consecutive_failures = 0
    last_update = 0

    while True:
        try:
            # Проверка интернета
            if not check_internet():
                log("⚠️ Нет интернета!")
                consecutive_failures += 1

                if consecutive_failures >= 3:
                    log("🔄 Попытка перезапуска VPN...")
                    update_subscription()
                    restart_hiddify()
                    consecutive_failures = 0
                    time.sleep(30)  # Ждем 30 сек после перезапуска

                time.sleep(CHECK_INTERVAL)
                continue

            # Проверка VPN соединения
            vpn_works = check_vpn_connection()

            if vpn_works:
                log("✅ VPN работает нормально")
                consecutive_failures = 0
            else:
                log("⚠️ VPN не работает!")
                consecutive_failures += 1

                if consecutive_failures >= 2:
                    log("🔄 Автоматическое восстановление...")
                    update_subscription()
                    time.sleep(5)
                    restart_hiddify()
                    consecutive_failures = 0
                    time.sleep(30)

            # Обновление конфигов каждые 2 часа
            current_time = time.time()
            if current_time - last_update > 7200:  # 2 часа
                log("🔄 Плановое обновление конфигов...")
                update_subscription()
                last_update = current_time

            time.sleep(CHECK_INTERVAL)

        except KeyboardInterrupt:
            log("⛔ Остановка VPN Watchdog")
            break
        except Exception as e:
            log(f"❌ Неожиданная ошибка: {e}")
            time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    main()
