# Проблема с GitHub Actions Watchdog

## Почему не работает каждую минуту

GitHub Actions cron имеет ограничения:
- ❌ Задержки до 15+ минут
- ❌ Может пропускать запуски при высокой нагрузке
- ❌ Не гарантирует точное время выполнения
- ❌ Не подходит для частого мониторинга

## Решения

### 1. Использовать внешний сервис (РЕКОМЕНДУЕТСЯ)

**cron-job.org** - бесплатный сервис для запуска задач:

1. Регистрируйся на https://cron-job.org
2. Создай новый cronjob:
   - URL: `https://api.github.com/repos/modrinthmodification-create/ownedvpn/dispatches`
   - Method: POST
   - Headers: 
     - `Authorization: token YOUR_GITHUB_TOKEN`
     - `Accept: application/vnd.github.v3+json`
   - Body: `{"event_type":"check-vpn"}`
   - Interval: Каждую минуту
3. Готово! Будет пинговать GitHub каждую минуту

**Как получить GitHub token:**
1. GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
2. Generate new token
3. Выбери scope: `repo` (full control)
4. Скопируй токен

### 2. Запустить на своем сервере

Если есть VPS - используй `server_watchdog.sh` из репозитория.

### 3. Оставить как есть (каждые 5 минут)

GitHub Actions будет проверять каждые 5 минут (с задержками).
Не идеально, но работает бесплатно.

## Текущая настройка

Сейчас watchdog настроен на:
- Каждые 5 минут через cron
- Ручной запуск через Actions
- Внешний триггер через API (для cron-job.org)
