# VPN Subscription для Hiddify

Автоматически обновляемая подписка VPN конфигураций из [vpn-configs-for-russia](https://github.com/igareck/vpn-configs-for-russia).

## 🚀 Быстрый старт

После первого запуска GitHub Actions, ссылка для подписки будет:

```
https://raw.githubusercontent.com/ВАШ_USERNAME/vpn-subscription/main/subscription.txt
```

Замени `ВАШ_USERNAME` на свой GitHub username.

## 📋 Инструкция по настройке

1. **Создай новый репозиторий на GitHub:**
   - Назови его `vpn-subscription` (или любое другое имя)
   - Сделай его публичным (Public)

2. **Загрузи эти файлы в репозиторий:**
   ```bash
   cd C:\scripts\vpn-subscription
   git init
   git add .
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin https://github.com/ВАШ_USERNAME/vpn-subscription.git
   git push -u origin main
   ```

3. **Включи GitHub Actions:**
   - Перейди в Settings → Actions → General
   - В разделе "Workflow permissions" выбери "Read and write permissions"
   - Сохрани изменения

4. **Запусти первое обновление:**
   - Перейди во вкладку "Actions"
   - Выбери "Update VPN Subscription"
   - Нажми "Run workflow" → "Run workflow"

5. **Получи ссылку для подписки:**
   - После завершения workflow появится файл `subscription.txt`
   - Твоя ссылка: `https://raw.githubusercontent.com/ВАШ_USERNAME/vpn-subscription/main/subscription.txt`

## 📱 Добавление в Hiddify

### Android/iOS
1. Открой Hiddify App
2. Нажми "+" → "Add from URL"
3. Вставь ссылку на subscription.txt
4. Готово!

### Windows/macOS
1. Открой Hiddify
2. Profiles → Add Profile → From URL
3. Вставь ссылку
4. Сохрани

## 🔄 Автообновление

GitHub Actions автоматически обновляет конфигурации каждые 2 часа. Hiddify будет подтягивать новые конфигурации при обновлении профиля.

## 🛠️ Настройка источников

Чтобы изменить источники конфигураций, отредактируй файл `.github/workflows/update-subscription.yml`:

```yaml
# Добавь или удали источники здесь:
curl -s "URL_К_КОНФИГУРАЦИЯМ" > temp/filename.txt
```

Доступные источники из vpn-configs-for-russia:
- `BLACK_VLESS_RUS_mobile.txt` - 150 лучших VLESS
- `BLACK_VLESS_RUS.txt` - полная VLESS подписка (1000-2000+)
- `BLACK_SS+All_RUS.txt` - SS, Hysteria2, VMess, Trojan
- `Vless-Reality-White-Lists-Rus-Mobile.txt` - CIDR конфиги

## 📊 Что включено

По умолчанию объединяются:
- ✅ VLESS Mobile (150 лучших конфигов)
- ✅ Shadowsocks + All Mix (SS, Hysteria2, VMess, Trojan)

Дубликаты автоматически удаляются.
"# ownedvpn" 
