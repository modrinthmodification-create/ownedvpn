# Настройка автоматического обновления через cron-job.org

## Проблема
GitHub Actions cron ненадежен - задержки до 30+ минут, пропускает запуски.

## Решение
Используем бесплатный сервис cron-job.org который будет пинговать GitHub API каждые 5 минут.

---

## Шаг 1: Создай GitHub Personal Access Token

1. Открой https://github.com/settings/tokens
2. Нажми **"Generate new token"** → **"Generate new token (classic)"**
3. Заполни:
   - **Note:** `cron-job.org VPN updater`
   - **Expiration:** `No expiration` (или 1 год)
   - **Scopes:** Поставь галочку только на `repo` (full control)
4. Нажми **"Generate token"**
5. **ВАЖНО:** Скопируй токен (он показывается только один раз!)
   - Формат: `ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`

---

## Шаг 2: Регистрация на cron-job.org

1. Открой https://cron-job.org/en/signup/
2. Зарегистрируйся (бесплатно)
3. Подтверди email

---

## Шаг 3: Создай Cron Job

1. Открой https://console.cron-job.org/jobs
2. Нажми **"Create cronjob"**
3. Заполни форму:

### Basic Settings:
- **Title:** `VPN Subscription Updater`
- **Address (URL):** 
  ```
  https://api.github.com/repos/modrinthmodification-create/ownedvpn/actions/workflows/update-subscription.yml/dispatches
  ```

### Schedule:
- **Every:** `5 minutes`
- **Days:** Все дни (оставь все галочки)

### Request Settings:
- **Request method:** `POST`
- **Request body:** 
  ```json
  {"ref":"main"}
  ```

### Headers:
Добавь 3 заголовка (нажми "+ Add header" 3 раза):

1. **Header name:** `Accept`
   **Value:** `application/vnd.github.v3+json`

2. **Header name:** `Authorization`
   **Value:** `token ВАШ_ТОКЕН_СЮДА`
   (замени `ВАШ_ТОКЕН_СЮДА` на токен из Шага 1)

3. **Header name:** `Content-Type`
   **Value:** `application/json`

### Advanced:
- **Save responses:** `Yes` (чтобы видеть ошибки)
- **Timeout:** `30 seconds`

4. Нажми **"Create cronjob"**

---

## Шаг 4: Проверка

1. В списке cronjobs нажми **"Run now"** на своем задании
2. Через 10 секунд проверь https://github.com/modrinthmodification-create/ownedvpn/actions
3. Должен появиться новый запуск workflow

---

## Готово!

Теперь cron-job.org будет пинговать GitHub каждые 5 минут и запускать обновление конфигов.

**Преимущества:**
- ✅ Надежно работает каждые 5 минут
- ✅ Бесплатно
- ✅ Можно видеть логи запросов
- ✅ Можно запустить вручную в любой момент

**Отключи GitHub Actions cron:**
Можешь оставить `workflow_dispatch` для ручного запуска, но убрать `schedule` из workflow.
