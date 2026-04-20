import requests
import sys
from datetime import datetime

SUBSCRIPTION_URL = "https://raw.githubusercontent.com/modrinthmodification-create/ownedvpn/main/subscription.txt"
LOCAL_FILE = "subscription.txt"

def log(message):
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {message}")

def check_internet():
    """Проверка интернета"""
    try:
        requests.get("https://www.google.com", timeout=5)
        log("✓ Интернет работает")
        return True
    except:
        log("✗ Нет интернета")
        return False

def check_vpn_availability():
    """Проверка доступности VPN конфигов"""
    blocked_sites = [
        "https://twitter.com",
        "https://facebook.com"
    ]

    for site in blocked_sites:
        try:
            response = requests.get(site, timeout=5)
            if response.status_code == 200:
                log(f"✓ {site} доступен")
                return True
        except:
            log(f"✗ {site} недоступен")
            continue

    return False

def update_subscription():
    """Обновление subscription файла"""
    try:
        log("Загрузка свежих конфигов...")
        response = requests.get(SUBSCRIPTION_URL, timeout=10)

        if response.status_code == 200:
            # Читаем текущий файл
            try:
                with open(LOCAL_FILE, 'r', encoding='utf-8') as f:
                    old_content = f.read()
            except:
                old_content = ""

            new_content = response.text

            # Проверяем изменились ли конфиги
            if old_content != new_content:
                with open(LOCAL_FILE, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                log("✓ Конфиги обновлены")
                return True
            else:
                log("✓ Конфиги актуальны")
                return False
        else:
            log(f"✗ Ошибка загрузки: HTTP {response.status_code}")
            return False
    except Exception as e:
        log(f"✗ Ошибка: {e}")
        return False

def main():
    log("🚀 VPN Watchdog запущен на GitHub Actions")

    # Проверка интернета
    if not check_internet():
        log("⚠ GitHub Actions не может подключиться к интернету")
        sys.exit(1)

    # Проверка VPN доступности
    vpn_works = check_vpn_availability()

    if vpn_works:
        log("✓ VPN конфиги работают")
    else:
        log("⚠ VPN может не работать, обновляем конфиги...")

    # Обновление конфигов
    updated = update_subscription()

    if updated:
        log("✓ Конфиги успешно обновлены и будут закоммичены")
    else:
        log("✓ Обновление не требуется")

    log("✓ Watchdog завершен")

if __name__ == "__main__":
    main()
