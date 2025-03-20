# icwt бэкенд: продукты и аналитика

## Установка
1. Установить виртуальное окружение, к примеру через стандартный модуль пайтон `python3 -m venv venv`
2. Активировать виртуальное окружение, юникс системы: `source venv/bin/activate` виндовс: `source venv\Scripts\activate`
3. Создать файл `.env` в корневой директории по примеру из репозитория
4. Из корневой директории запустить `docker compose up --build -d` (в зависимости от версии докер композ `docker-compose up --build -d`)
5. По стандарту апи будет доступен по `http://localhost:44444`, порт проброшен из контейнера

## CRUD операции

### GET `/api/v1/products`
Описание: Получить список всех продуктов (кешируется)
```
curl --url "http://localhost:44444/api/v1/products" \
    --request GET
```
Параметры запроса:
- `limit: int` [опционально] ограничивает количество выданных запросов, стандарт - `50`, максимально - `100`
- `offset: int` [опционально] указывает оффсет для выданных запросов, стандарт - `0`

Ответ:
- `200` ответ получен

Пример ответа:
```
{
  "limit": 50,
  "offset": 0,
  "data": [
    {
      "id": 1,
      "category_id": 1,
      "name": "product"
    }
  ]
}
```

### GET `/api/v1/products/{product_id}`
Описание: Получить информацию о продукте по `id`
```
curl --url "http://localhost:44444/api/v1/products/1" \
    --request GET
```
Ответ:
- `200` если продукт найден
- `404` если продукт не найден

Пример ответа:
```
{
  "id": 1,
  "category_id": 1,
  "name": "product"
}
```

### POST `/api/v1/products`
Описание: Создать новый продукт
```
curl --url "http://localhost:44444/api/v1/products" \
    --request POST \
    --header "Content-Type: application/json" \
    --data '{"name": "new_product", "category_id": 2}'
```
Ответ:
- `201` продукт успешно создан

Пример ответа:
```
{
  "id": 2,
  "name": "new_product",
  "category_id": 2
}
```

### PUT `/api/v1/products/{product_id}`
Описание: Обновить существующий продукт
```
curl --url "http://localhost:44444/api/v1/products/1" \
    --request PUT \
    --header "Content-Type: application/json" \
    --data '{"name": "updated_product", "category_id": 3}'
```
Ответ:
- `200` продукт успешно обновлён

Пример ответа:
```
{
  "id": 1,
  "name": "updated_product",
  "category_id": 3
}
```

### DELETE `/api/v1/products/{product_id}`
Описание: Удалить продукт по `id`
```
curl --url "http://localhost:44444/api/v1/products/1" \
    --request DELETE
```
Ответ:
- `204` продукт успешно удалён

## Аналитика продаж

### GET `/api/v1/sales/total`
Описание: Получить общую сумму продаж за период (по умолчанию за последние 180 дней)
```
curl --url "http://localhost:44444/api/v1/sales/total?start_date=2023-01-01&end_date=2023-06-30" \
    --request GET
```
Параметры запроса:
- `start_date: str` [опционально] дата начала периода (ISO формат)
- `end_date: str` [опционально] дата окончания периода (ISO формат)

Ответ:
- `200` данные получены

Пример ответа:
```
{
  "start_date": "2023-01-01",
  "end_date": "2023-06-30",
  "total": 50000
}
```

### GET `/api/v1/sales/top-products`
Описание: Получить топ-продукты по продажам за период
```
curl --url "http://localhost:44444/api/v1/sales/top-products?start_date=2023-01-01&end_date=2023-06-30&limit=5" \
    --request GET
```
Параметры запроса:
- `start_date: str` [опционально] дата начала периода (ISO формат)
- `end_date: str` [опционально] дата окончания периода (ISO формат)
- `limit: int` [опционально] количество топ-продуктов, стандарт - `10`

Ответ:
- `200` данные получены

Пример ответа:
```
{
  "start_date": "2023-01-01",
  "end_date": "2023-06-30",
  "limit": 5,
  "data": [
    {
      "name": "product_1",
      "sold_amount": 200
    },
    {
      "name": "product_2",
      "sold_amount": 150
    }
  ]
}
```

