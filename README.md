# Построение H-S диаграммы

## Получение необходимых данных

1. Перходим на сайт базы NIST https://webbook.nist.gov/chemistry/fluid/

2. Выбираем необходимое вещество (На примере будет Trichlorofluoromethane (R11)) 

3. Выбираем системы измерений:

![alt text](/docs/USE_SI.png)


4. Нажимаем Press to Continue

5. Теперь переходит в поисковую строку и находим `ID` вещества (`ID=C75694`)

![alt text](/docs//ID.png)

6. В `config.py` указать свой `ID` вещества, а так же граничные велчины для получения данных.

7. Готово!

## Программа:
![alt text](/docs/config.png)


Получение данных происходит при запрос на сервер и обработки его ответа, поэтому добавлены сообщения о статусе запроса

![alt text](/docs/saturation_code.png)

![alt text](/docs/saturation_line.png)

Тоже самое с изотермами и изобарами:

![alt text](/docs/isothermal.png)

## H-S диаграмма:

Для удачного построения H-S диагрммы необходимо зайти в `plotter.py` и указать необходимые максимальные H и S значения, далее приблизить график в нужной области и сохранить изображение.

![alt text](/docs/H-S_small.png)

### Сохранение данных:

Для быстрой и удобной работы с графиком добавлена загрузка полученных данных в `/data`.

## Цикл Ренкина:

В файле `renkine.ipynb` можно построить цикл ренкина указав 5 точку цикла (После перегрева, перед турбиной).


![alt text](/docs/5_point.png)

Далее код рассчитает цикл и сохранит данные:

![alt text](/docs/get_renkine.png)

![alt text](/docs/renkine.png)

![alt text](/docs/4_6_renkine.png)

![alt text](/docs/1_2_renkine.png)

![alt text](/docs/3_renkine.png)

## Работа с кодом:

Установка завистимостей:

```bash
pip install -r requirements.txt
```