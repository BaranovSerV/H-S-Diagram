# Построение H-S диаграммы

## Получение необходимых данных

1. Перходим на сайт базы NIST https://webbook.nist.gov/chemistry/fluid/

2. Выбираем необходимое вещество (На примере будет Trichlorofluoromethane (R11)) 

3. Выбираем системы измерений:

![alt text](/docs/image.png)


4. Нажимаем Press to Continue

5. Теперь переходит в поисковую строку и находим ID вещества (ID=C75694)

![alt text](/docs//ID.png)

6. В main.ipynb указать свой ID вещества

7. Готово!

## Программа:

![alt text](/docs/ID_code.png)

Получение данных происходит при запрос на сервер и обработки его ответа, поэтому добавлены сообщения о статусе запроса

![alt text](/docs/saturation.png)

![alt text](/docs/saturation_line.png)

Тоже самое с изотермами и изобарами:

![alt text](/docs/isothermal.png)

## H-S диаграмма:

![alt text](/docs/HS.png)

## Работа с кодом:

Установка завистимостей:

```bash
pip install -r requirements.txt
```