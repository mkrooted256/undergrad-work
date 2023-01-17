# Lab10. Apache Spark
Mykhailo Koreshkov, FI-91

## 0. Середовище
Роботу виконував в докер контейнері.

Запускаю його наступним чином
```
docker run -it -v C:\Users\mkrooted\Uni\7-highload\lab10:/app apache/spark-py:v3.3.1 bash
```

## 1. Код
Можна подивитися в [mapreduce.py](mapreduce.py)

## 2. Виконання
В bash всередині контейнера:
```
/opt/spark/bin/spark-submit --driver-memory 2G --executor-memory 2G /app/mapreduce.py
```

Без `--memory-...` параметрів видавало OutOfMemory помилки.

## 3. Результати
1. Загальна кількість згадувань
```
+-----------+---------------+
|       lang|sum(occurences)|
+-----------+---------------+
|    haskell|            897|
|         c#|           3034|
|       perl|           3986|
|       ruby|           1441|
| javascript|          11227|
|        css|           6835|
|    clojure|            157|
|      scala|           1210|
|        c++|           3097|
|objective-c|            651|
|     groovy|            208|
|       java|          19864|
|        php|          27241|
|     matlab|           1542|
|     python|           3078|
+-----------+---------------+
```

2. Кількість статей, що згадали
```
+-----------+-------------+
|       lang|sum(bOccured)|
+-----------+-------------+
|    haskell|          128|
|         c#|          902|
|       perl|          838|
|       ruby|          304|
| javascript|         1770|
|        css|          634|
|    clojure|           60|
|      scala|          387|
|        c++|          560|
|objective-c|          113|
|     groovy|           62|
|       java|         2031|
|        php|         1433|
|     matlab|          344|
|     python|          580|
+-----------+-------------+
```

