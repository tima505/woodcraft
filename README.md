# ДРЕВОПРО - Система управления производством

Полноценное веб-приложение для управления производством деревянных изделий.

## Структура проекта
- `woodcraft_back/` - Backend на Django REST Framework
- `woodcraft-front/` - Frontend на Vue 3 + Pinia + Vue Router

## Запуск Backend (Django)

1. Откройте терминал в папке `woodcraft_back`
2. Активируйте виртуальное окружение:
   ```bash
   .\venv\Scripts\activate
   ```
   *(Если venv нет, создайте его: `python -m venv venv` и установите зависимости `pip install django djangorestframework django-cors-headers`)*
3. Примените миграции (если еще не применены):
   ```bash
   python manage.py migrate
   ```
4. Загрузите тестовые данные (админ, рабочие, заказы):
   ```bash
   python manage.py initial_data
   ```
5. Запустите сервер:
   ```bash
   python manage.py runserver
   ```
Бэкенд будет доступен по адресу `http://localhost:8000/api/`

## Запуск Frontend (Vue.js)

1. Откройте второй терминал в папке `woodcraft-front`
2. Установите зависимости (если еще не установлены):
   ```bash
   npm install
   ```
3. Запустите dev-сервер:
   ```bash
   npm run dev
   ```
4. Откройте ссылку в браузере (обычно `http://localhost:5173/`).

## Учетные данные для тестирования (из initial_data)
- **Администратор**
  Логин: `admin`
  Пароль: `admin`
- **Рабочий 1** (Первые этапы)
  Логин: `worker1`
  Пароль: `password123`
- **Рабочий 2** (Последние этапы)
  Логин: `worker2`
  Пароль: `password123`
