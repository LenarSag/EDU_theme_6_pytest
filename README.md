# EDU_theme_6_pytest

# Trading API

## Описание

Trading API предоставляет доступ к данным о торговых днях, динамике торгов и результатах торгов. API реализовано с использованием FastAPI и поддерживает авторизацию через JWT-токены.

Тесты pytest проверяют enpoint приложения. Тесты выолняются асинхронно, при помощи pytest.asyncio, для тестов создается временная in-memory база данных, которая удаляется после тестов.

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

### Запуск тестов
```sh
pytest
```

