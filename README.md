# EDU_theme_5_fastapi


# Trading API

## Описание

Trading API предоставляет доступ к данным о торговых днях, динамике торгов и результатах торгов. API реализовано с использованием FastAPI и поддерживает авторизацию через JWT-токены.

## Установка и запуск

### Требования
- Python 3.12+
- PostgreSQL
- Redis

### Перед установкой зависимостей рекомендуется создать виртуальное окружение:

```sh
python -m venv venv
source venv/bin/activate  # Для macOS/Linux
venv\Scripts\activate    # Для Windows
```

### Установка зависимостей
```sh
pip install -r requirements.txt
```

### Запуск сервера
```sh
python main.py
```

## Эндпоинты

### Регистрация пользователя
**POST /register**
- Регистрирует нового пользователя.
- **Тело запроса:**
  ```json
  {
    "username": "example_user",
    "email": "user@example.com",
    "password": "securepassword"
  }
  ```
- **Ответ:**
  ```json
  {
    "id": 1,
    "username": "example_user",
    "email": "user@example.com"
  }
  ```

### Получение токена
**POST /token**
- Авторизует пользователя и возвращает JWT-токен.
- **Тело запроса:**
  ```json
  {
    "email": "user@example.com",
    "password": "securepassword"
  }
  ```
- **Ответ:**
  ```json
  {
    "access_token": "jwt_token_here",
    "token_type": "Bearer"
  }
  ```

### Получение списка последних торговых дней
**GET /get-last-trading-dates**
- **Фильтры:** количество последних торговых дней.
- **Ответ:** JSON-список дат последних торговых дней.

GET http://127.0.0.1:8000/api/v1/trades/get-trading-results?size=5&page=3

  ```json
  {
    "items": [{"id": 12127, "exchange_product_id": "A592AVM005A", "exchange_product_name": "Бензин (АИ-92-К5) по ГОСТ, СН КНПЗ (самовывоз автотранспортом)", "oil_id": "A592", "delivery_basis_id": "AVM", "delivery_basis_name": "СН КНПЗ", "delivery_type_id": "A", "volume": 25, "total": 1392500, "count": 3, "date": "2024-01-09", "created_on": "2025-01-01 12:26:15.018445", "updated_on": null}, {"id": 12128, "exchange_product_id": "A592BIN061F", "exchange_product_name": "Бензин (АИ-92-К5) по ГОСТ, ст. Биклянь (ст. отправления)", "oil_id": "A592", "delivery_basis_id": "BIN", "delivery_basis_name": "ст. Биклянь", "delivery_type_id": "F", "volume": 549, "total": 21271493, "count": 5, "date": "2024-01-09", "created_on": "2025-01-01 12:26:15.018445", "updated_on": null}, {"id": 12129, "exchange_product_id": "A592BRF005A", "exchange_product_name": "Бензин (АИ-92-К5) по ГОСТ, Брянская НБ (самовывоз автотранспортом)", "oil_id": "A592", "delivery_basis_id": "BRF", "delivery_basis_name": "Брянская НБ", "delivery_type_id": "A", "volume": null, "total": null, "count": null, "date": "2024-01-09", "created_on": "2025-01-01 12:26:15.018445", "updated_on": null}, {"id": 12130, "exchange_product_id": "A592BSA005A", "exchange_product_name": "Бензин (АИ-92-К5) по ГОСТ, Балашовская НБ (самовывоз автотранспортом)", "oil_id": "A592", "delivery_basis_id": "BSA", "delivery_basis_name": "Балашовская НБ", "delivery_type_id": "A", "volume": null, "total": null, "count": null, "date": "2024-01-09", "created_on": "2025-01-01 12:26:15.018445", "updated_on": null}, {"id": 12116, "exchange_product_id": "A100ANK060F", "exchange_product_name": "Бензин (АИ-100-К5), Ангарск-группа станций (ст. отправления)", "oil_id": "A100", "delivery_basis_id": "ANK", "delivery_basis_name": "Ангарск-группа станций", "delivery_type_id": "F", "volume": 60, "total": 3739920, "count": 1, "date": "2024-01-09", "created_on": "2025-01-01 12:26:15.018445", "updated_on": null}], "total": 118600, 
    "page": 3, 
    "size": 5, 
    "pages": 23720
  }
  ```


### Получение динамики торгов
**GET /get-dynamics**
- **Фильтры:** oil_id, delivery_type_id, delivery_basis_id, start_date, end_date.
- **Ответ:** JSON-список торгов за указанный период.

### Получение результатов торгов
**GET /get-trading-results**
- **Фильтры:** oil_id, delivery_type_id, delivery_basis_id.
- **Ответ:** JSON-список последних торгов.

GET http://127.0.0.1:8000/api/v1/trades/get-last-trading-dates?last_days=34&size=3&page=2

  ```json
  {
    "items": [{"id": 117566, "exchange_product_id": "A001KRU060F", "exchange_product_name": "Бензин (АИ-100-К5), ст. Круглое Поле (ст. отправления)", "oil_id": "A001", "delivery_basis_id": "KRU", "delivery_basis_name": "ст. Круглое Поле", "delivery_type_id": "F", "volume": null, "total": null, "count": null, "date": "2024-11-25", "created_on": "2025-01-01 12:28:17.401514", "updated_on": null}, {"id": 117568, "exchange_product_id": "A100STI060F", "exchange_product_name": "Бензин (АИ-100-К5), ст. Стенькино II (ст. отправления)", "oil_id": "A100", "delivery_basis_id": "STI", "delivery_basis_name": "ст. Стенькино II", "delivery_type_id": "F", "volume": null, "total": null, "count": null, "date": "2024-11-25", "created_on": "2025-01-01 12:28:17.401514", "updated_on": null}, {"id": 117571, "exchange_product_id": "A592ABS005A", "exchange_product_name": "Бензин (АИ-92-К5) по ГОСТ, НБ Абаканская (самовывоз автотранспортом)", "oil_id": "A592", "delivery_basis_id": "ABS", "delivery_basis_name": "НБ Абаканская", "delivery_type_id": "A", "volume": null, "total": null, "count": null, "date": "2024-11-25", "created_on": "2025-01-01 12:28:17.401514", "updated_on": null}], 
    "total": 13150, 
    "page": 2, 
    "size": 3, 
    "pages": 4384
  }
  ```

## Кэширование
API использует Redis для кэширования данных торгов, что позволяет ускорить обработку запросов.

## Авторизация
Все эндпоинты, связанные с получением данных о торгах, требуют аутентификации через Bearer-токен.








