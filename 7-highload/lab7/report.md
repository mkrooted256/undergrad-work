# 7-Highload. Lab7.
Mykhailo Koreshkov, FI-91

## 1. Cluster setup

Перша нода залишилась з попереднього завдання.

```
(sci) PS C:\Windows\system32> docker run --name cas1 -d --network cas --ip 192.17.2.3 -e CASSANDRA_SEEDS="192.17.2.2" cassandra:4.1.0
68082a7dea1952d6ff156831d616cd32ace29d2530024ec38f636da4605ae27f
(sci) PS C:\Windows\system32> docker run --name cas2 -d --network cas --ip 192.17.2.4 -e CASSANDRA_SEEDS="192.17.2.2" cassandra:4.1.0
e8a7fd9e23621543ab7d2409ce2c8c6cf2ce76df230f2240c4759c8eff921bcd
```

На першій ноді `cas`:
```
root@b8f148257686:/# nodetool status
Datacenter: datacenter1
=======================
Status=Up/Down
|/ State=Normal/Leaving/Joining/Moving
--  Address     Load        Tokens  Owns (effective)  Host ID                               Rack
UN  192.17.2.4  186.17 KiB  16      100.0%            f0b75d5a-fbfd-4cc3-9fdc-3244b5013cfe  rack1
UN  192.17.2.3  164.44 KiB  16      100.0%            257e4107-1374-418f-8df4-4a533abc8b91  rack1
UN  192.17.2.2  314.31 KiB  16      100.0%            1350c341-d879-4a9d-b761-032a79c949ef  rack1
```

## 3. та 4. Створення keyspaces та таблиць в них

```
cqlsh> CREATE KEYSPACE Lab7r3 WITH REPLICATION = {'replication_factor': 3, 'class': 'SimpleStrategy'};
cqlsh> CREATE KEYSPACE Lab7r2 WITH REPLICATION = {'replication_factor': 2, 'class': 'SimpleStrategy'};
cqlsh> CREATE KEYSPACE Lab7r1 WITH REPLICATION = {'replication_factor': 1, 'class': 'SimpleStrategy'};

cqlsh> CREATE TABLE Lab7r1.A ( id int, str text, PRIMARY KEY (id) );
cqlsh> CREATE TABLE Lab7r2.A ( id int, str text, PRIMARY KEY (id) );
cqlsh> CREATE TABLE Lab7r3.A ( id int, str text, PRIMARY KEY (id) );
```

## 5. Спробуйте писати і читати на / та з різних нод

З головної ноди:
```
(sci) PS C:\Windows\system32> docker exec -it cas cqlsh
...
cqlsh> insert into Lab7r3.A (id, str) values (100, 'Lorem 1');
cqlsh> insert into Lab7r3.A (id, str) values (200, 'Lorem 2');
cqlsh> insert into Lab7r1.A (id, str) values (100, 'Lorem 1');
cqlsh> insert into Lab7r2.A (id, str) values (100, 'Lorem 1');

cqlsh> select * from Lab7r1.A;

 id  | str
-----+---------
 100 | Lorem 1

(1 rows)
cqlsh> select * from Lab7r2.A;

 id  | str
-----+---------
 100 | Lorem 1

(1 rows)
cqlsh> select * from Lab7r3.A;

 id  | str
-----+---------
 200 | Lorem 2
 100 | Lorem 1

(2 rows)
```

З `cas1`:
```
(sci) PS C:\Windows\system32> docker exec -it cas1 cqlsh
Connected to Test Cluster at 127.0.0.1:9042
[cqlsh 6.1.0 | Cassandra 4.1.0 | CQL spec 3.4.6 | Native protocol v5]
Use HELP for help.
cqlsh> select * from Lab7r1.A;

 id  | str
-----+---------
 100 | Lorem 1

(1 rows)
cqlsh> select * from Lab7r2.A;

 id  | str
-----+---------
 100 | Lorem 1

(1 rows)
cqlsh> select * from Lab7r3.A;

 id  | str
-----+---------
 200 | Lorem 2
 100 | Lorem 1

(2 rows)
```

Далі вже без логів, бо займає багато місця.

- insert на cas1 в різні таблиці
- select на cas  
    Видно всі нові дані
- select на cas2
    Видно всі нові дані

## 6. Вставте дані в створені таблиці і подивіться на їх розподіл по вузлах кластера

```
cqlsh> select * from Lab7r1.A;

 id   | str
------+---------
 1001 |    null
  302 |    null
  203 |    null
  100 | Lorem 1
  102 |    null
  303 |    null
  101 |    cas1
 1002 |    null
  202 |    null
  103 |    null
```

І те саме в інших таблицях.

Розподіл по вузлах:

> З документації:  
    SimpleStrategy places the first replica on a node determined by the partitioner. Additional replicas are placed on the next nodes clockwise in the ring without considering topology (rack or datacenter location).

```
root@b8f148257686:/# nodetool status lab7r1
Datacenter: datacenter1
=======================
Status=Up/Down
|/ State=Normal/Leaving/Joining/Moving
--  Address     Load        Tokens  Owns (effective)  Host ID                               Rack
UN  192.17.2.4  273.57 KiB  16      35.7%             f0b75d5a-fbfd-4cc3-9fdc-3244b5013cfe  rack1
UN  192.17.2.3  267.37 KiB  16      31.6%             257e4107-1374-418f-8df4-4a533abc8b91  rack1
UN  192.17.2.2  295.93 KiB  16      32.7%             1350c341-d879-4a9d-b761-032a79c949ef  rack1

root@b8f148257686:/# nodetool status lab7r2
Datacenter: datacenter1
=======================
Status=Up/Down
|/ State=Normal/Leaving/Joining/Moving
--  Address     Load        Tokens  Owns (effective)  Host ID                               Rack
UN  192.17.2.4  273.57 KiB  16      76.0%             f0b75d5a-fbfd-4cc3-9fdc-3244b5013cfe  rack1
UN  192.17.2.3  267.37 KiB  16      59.3%             257e4107-1374-418f-8df4-4a533abc8b91  rack1
UN  192.17.2.2  295.93 KiB  16      64.7%             1350c341-d879-4a9d-b761-032a79c949ef  rack1

root@b8f148257686:/# nodetool status lab7r3
Datacenter: datacenter1
=======================
Status=Up/Down
|/ State=Normal/Leaving/Joining/Moving
--  Address     Load        Tokens  Owns (effective)  Host ID                               Rack
UN  192.17.2.4  273.57 KiB  16      100.0%            f0b75d5a-fbfd-4cc3-9fdc-3244b5013cfe  rack1
UN  192.17.2.3  267.37 KiB  16      100.0%            257e4107-1374-418f-8df4-4a533abc8b91  rack1
UN  192.17.2.2  295.93 KiB  16      100.0%            1350c341-d879-4a9d-b761-032a79c949ef  rack1
```

Як це можна трактувати:
- В r1 маємо мінімальну реплікацію. Кожен вузол зберігає лише свої дані. ("свої" дані визначаються за хешсумами ключа)
- В r3 маємо повну реплікацію. Кожен вузол зберігає всі дані.
- В r2 щось середнє

## 7. Для якогось запису з кожного з кейспейсу виведіть ноди на яких зберігаються дані

```
root@b8f148257686:/# nodetool getendpoints lab7r1 a 100
192.17.2.4
root@b8f148257686:/# nodetool getendpoints lab7r2 a 100
192.17.2.4
192.17.2.3
root@b8f148257686:/# nodetool getendpoints lab7r3 a 100
192.17.2.4
192.17.2.3
192.17.2.2
```

Бачимо, що кількість нод рівна рівню реплікації.

## 8. 

Вимикаю ноду `cas2`.

```
cqlsh> consistency ONE
Consistency level set to ONE.
cqlsh> select * from Lab7r1.A;
NoHostAvailable: ('Unable to complete the operation against any hosts', {<Host: 127.0.0.1:9042 datacenter1>: Unavailable('Error from server: code=1000 [Unavailable exception] message="Cannot achieve consistency level ONE" info={\'consistency\': \'ONE\', \'required_replicas\': 1, \'alive_replicas\': 0}')})
cqlsh> select * from Lab7r2.A;

 id   | str
------+---------
  201 |    null
 1001 |    null
  302 |    null
  100 | Lorem 1
  102 |    null
 1002 |    null
  301 |    null
  202 |    null
  103 |    null

(9 rows)
cqlsh> select * from Lab7r3.A;

 id   | str
------+---------
 1001 |    null
  302 |    null
  203 |    null
  200 | Lorem 2
  100 | Lorem 1
  102 |    null
 1002 |    null
  301 |    null
  202 |    null
  103 |    null

(10 rows)
```

Перший селект неможливий, бо третина рядків зараз недоступні, бо зберігаються лише на вимкненій ноді. Інші селекти працюють, бо кожен запис має принаймні 1 (ONE) ноду.

Тепер знайду якийсь запис на увімкеній ноді (101)
```
root@b8f148257686:/# nodetool getendpoints lab7r1 a 101
192.17.2.2
```

```
cqlsh> select * from Lab7r1.A where id=101;

 id  | str
-----+------
 101 | cas1
```

Дані, що належать іншим нодам, все ще доступні.

---

```
cqlsh> consistency TWO
Consistency level set to TWO.
cqlsh> select * from Lab7r1.A;
NoHostAvailable: ('Unable to complete the operation against any hosts', {<Host: 127.0.0.1:9042 datacenter1>: Unavailable('Error from server: code=1000 [Unavailable exception] message="Cannot achieve consistency level TWO" info={\'consistency\': \'TWO\', \'required_replicas\': 2, \'alive_replicas\': 1}')})
cqlsh> select * from Lab7r2.A;
NoHostAvailable: ('Unable to complete the operation against any hosts', {<Host: 127.0.0.1:9042 datacenter1>: Unavailable('Error from server: code=1000 [Unavailable exception] message="Cannot achieve consistency level TWO" info={\'consistency\': \'TWO\', \'required_replicas\': 2, \'alive_replicas\': 1}')})
cqlsh> select * from Lab7r3.A;

 id   | str
------+---------
 1001 |    null
  302 |    null
  203 |    null
  200 | Lorem 2
  100 | Lorem 1
  102 |    null
 1002 |    null
  301 |    null
  202 |    null
  103 |    null

(10 rows)
```

Звісно, тепер два перших селекта не працюють. 

```
root@b8f148257686:/# nodetool getendpoints lab7r2 a 1001
192.17.2.3
192.17.2.2
```

```
cqlsh> select * from Lab7r1.A where id=1001;
NoHostAvailable: ('Unable to complete the operation against any hosts', {<Host: 127.0.0.1:9042 datacenter1>: Unavailable('Error from server: code=1000 [Unavailable exception] message="Cannot achieve consistency level TWO" info={\'consistency\': \'TWO\', \'required_replicas\': 2, \'alive_replicas\': 1}')})
cqlsh> select * from Lab7r2.A where id=1001;

 id   | str
------+------
 1001 | null
```

Бачимо, що дані, які не зберігаються на відключеній ноді, все ще доступні. Але перша таблиця повністю недоступна, бо рівень консистентності 2 недосяжний при рівні реплікації 1.

---

```
cqlsh> select * from Lab7r1.A;
NoHostAvailable: ('Unable to complete the operation against any hosts', {<Host: 127.0.0.1:9042 datacenter1>: Unavailable('Error from server: code=1000 [Unavailable exception] message="Cannot achieve consistency level QUORUM" info={\'consistency\': \'QUORUM\', \'required_replicas\': 1, \'alive_replicas\': 0}')})
cqlsh> select * from Lab7r2.A;
NoHostAvailable: ('Unable to complete the operation against any hosts', {<Host: 127.0.0.1:9042 datacenter1>: Unavailable('Error from server: code=1000 [Unavailable exception] message="Cannot achieve consistency level QUORUM" info={\'consistency\': \'QUORUM\', \'required_replicas\': 2, \'alive_replicas\': 1}')})
cqlsh> select * from Lab7r3.A;

 id   | str
------+---------
 1001 |    null
  302 |    null
  203 |    null
  200 | Lorem 2
  100 | Lorem 1
  102 |    null
 1002 |    null
  301 |    null
  202 |    null
  103 |    null

(10 rows)
```

QUORUM тут еквівалентно TWO, тому нічого нового.

---

> Note: `192.17.2.4` is down

```
root@b8f148257686:/# nodetool getendpoints lab7r1 a 100
192.17.2.4
```

```
cqlsh> consistency ONE
Consistency level set to ONE.
cqlsh> insert into Lab7r1.A (id, str) values (100, 'haha');
NoHostAvailable: ('Unable to complete the operation against any hosts', {<Host: 127.0.0.1:9042 datacenter1>: Unavailable('Error from server: code=1000 [Unavailable exception] message="Cannot achieve consistency level ONE" info={\'consistency\': \'ONE\', \'required_replicas\': 1, \'alive_replicas\': 0}')})
cqlsh> insert into Lab7r2.A (id, str) values (100, 'haha');
cqlsh> insert into Lab7r1.A (id, str) values (101, 'haha');
```

Бачимо, що інсерт запису з ключем, що відповідає вимкненій ноді, не вдався.


```
root@b8f148257686:/# nodetool getendpoints lab7r1 a 101
192.17.2.2
root@b8f148257686:/# nodetool getendpoints lab7r2 a 102
192.17.2.4
192.17.2.2
root@b8f148257686:/# nodetool getendpoints lab7r2 a 1001
192.17.2.3
192.17.2.2
root@b8f148257686:/# nodetool getendpoints lab7r2 a 1002
192.17.2.4
192.17.2.3
```

```
cqlsh> consistency QUORUM
Consistency level set to QUORUM.
cqlsh> insert into Lab7r1.A (id, str) values (101, 'haha1');
cqlsh> insert into Lab7r1.A (id, str) values (102, 'haha1');
NoHostAvailable: ('Unable to complete the operation against any hosts', {<Host: 127.0.0.1:9042 datacenter1>: Unavailable('Error from server: code=1000 [Unavailable exception] message="Cannot achieve consistency level QUORUM" info={\'consistency\': \'QUORUM\', \'required_replicas\': 1, \'alive_replicas\': 0}')})
cqlsh> insert into Lab7r2.A (id, str) values (1001, 'haha1');
cqlsh> insert into Lab7r2.A (id, str) values (1002, 'haha1');
NoHostAvailable: ('Unable to complete the operation against any hosts', {<Host: 127.0.0.1:9042 datacenter1>: Unavailable('Error from server: code=1000 [Unavailable exception] message="Cannot achieve consistency level QUORUM" info={\'consistency\': \'QUORUM\', \'required_replicas\': 2, \'alive_replicas\': 1}')})
```

Інсерт вдався лише для тих ключів, які не відповідають вимкненій ноді.
Інсерт в r3 вдасться завжди.

## 9. Drop connection

```
(sci) PS C:\Windows\system32> docker network disconnect cas cas1
(sci) PS C:\Windows\system32> docker network disconnect cas cas2
(sci) PS C:\Windows\system32> docker exec -it cas bash
root@b8f148257686:/# nodetool status
Datacenter: datacenter1
=======================
Status=Up/Down
|/ State=Normal/Leaving/Joining/Moving
--  Address     Load        Tokens  Owns  Host ID                               Rack
DN  192.17.2.4  273.57 KiB  16      ?     f0b75d5a-fbfd-4cc3-9fdc-3244b5013cfe  rack1
DN  192.17.2.3  267.37 KiB  16      ?     257e4107-1374-418f-8df4-4a533abc8b91  rack1
UN  192.17.2.2  280.43 KiB  16      ?     1350c341-d879-4a9d-b761-032a79c949ef  rack1
(sci) PS C:\Windows\system32> docker exec -it cas1 bash
root@68082a7dea19:/# nodetool status
Datacenter: datacenter1
=======================
Status=Up/Down
|/ State=Normal/Leaving/Joining/Moving
--  Address     Load        Tokens  Owns  Host ID                               Rack
DN  192.17.2.4  273.57 KiB  16      ?     f0b75d5a-fbfd-4cc3-9fdc-3244b5013cfe  rack1
UN  192.17.2.3  267.37 KiB  16      ?     257e4107-1374-418f-8df4-4a533abc8b91  rack1
DN  192.17.2.2  280.43 KiB  16      ?     1350c341-d879-4a9d-b761-032a79c949ef  rack1
```

## 10. 

Запис.

```
(cas)
cqlsh> use lab7r3;
cqlsh:lab7r3> consistency one;
Consistency level set to ONE.
cqlsh:lab7r3> insert into A (id, str) values (42, 'thanks for all the fish');
cqlsh:lab7r3> insert into A (id, str) values (43, 'false');
cqlsh:lab7r3> insert into A (id, str) values (44, 'true');

(cas1)
cqlsh> use lab7r3;
cqlsh:lab7r3> consistency ONE
Consistency level set to ONE.
cqlsh:lab7r3> insert into A (id, str) values (42, 'it is not the answer');
cqlsh:lab7r3> insert into A (id, str) values (43, 'true');
cqlsh:lab7r3> insert into A (id, str) values (44, 'true');

(cas2)
cqlsh> use lab7r3;
cqlsh:lab7r3> consistency ONE
Consistency level set to ONE.
cqlsh:lab7r3> insert into A (id, str) values (42, 'and now for something completely different');
cqlsh:lab7r3> insert into A (id, str) values (43, 'true');
cqlsh:lab7r3> insert into A (id, str) values (44, 'false');

```

Відновлення зв'язку

```
(sci) PS C:\Windows\system32> docker network connect --ip 192.17.2.4 cas cas2
(sci) PS C:\Windows\system32> docker network connect --ip 192.17.2.3 cas cas1
(sci) PS C:\Windows\system32> docker exec -it cas nodetool status
Datacenter: datacenter1
=======================
Status=Up/Down
|/ State=Normal/Leaving/Joining/Moving
--  Address     Load        Tokens  Owns  Host ID                               Rack
UN  192.17.2.4  251.04 KiB  16      ?     f0b75d5a-fbfd-4cc3-9fdc-3244b5013cfe  rack1
UN  192.17.2.3  267.37 KiB  16      ?     257e4107-1374-418f-8df4-4a533abc8b91  rack1
UN  192.17.2.2  280.43 KiB  16      ?     1350c341-d879-4a9d-b761-032a79c949ef  rack1
```

Результат

```
(cas)
cqlsh:lab7r3> select * from A where id in (42,43,44);

 id | str
----+--------------------------------------------
 42 | and now for something completely different
 43 |                                       true
 44 |                                      false

(cas1)
cqlsh:lab7r3> select * from A where id in (42,43,44);

 id | str
----+--------------------------------------------
 42 | and now for something completely different
 43 |                                       true
 44 |                                      false

(cas2)
cqlsh:lab7r3> select * from A where id in (42,43,44);

 id | str
----+--------------------------------------------
 42 | and now for something completely different
 43 |                                       true
 44 |                                      false


```

Конфлікти всіх записів вирішено згідно принципу Last Write Wins - залишаємо найновіше значення.  
Для ключа 44 кворум мало значення true, але вирішено залишити false, бо цей запис відбувся останнім.

## 12.


```
cqlsh:lab7r3> insert into A (id, str) values (50, 'a');

cqlsh:lab7r3> UPDATE A SET str = 'b' WHERE id=50 IF str = 'a';

 [applied]
-----------
      True

cqlsh:lab7r3> UPDATE A SET str = 'b' WHERE id=50 IF str = 'a';

 [applied] | str
-----------+-----
     False |   b

cqlsh:lab7r3> insert into A (id, str) values (51, 'b') IF not exists;

 [applied]
-----------
      True

cqlsh:lab7r3> insert into A (id, str) values (51, 'c') IF not exists;

 [applied] | id | str
-----------+----+-----
     False | 51 |   b

```

Вимикаємо зв'язок

```
cqlsh:lab7r3> consistency TWO
Consistency level set to TWO.
cqlsh:lab7r3> UPDATE A SET str = 'b' WHERE id=50 IF str = 'a';
NoHostAvailable: ('Unable to complete the operation against any hosts', {<Host: 127.0.0.1:9042 datacenter1>: Unavailable('Error from server: code=1000 [Unavailable exception] message="Cannot achieve consistency level SERIAL" info={\'consistency\': \'SERIAL\', \'required_replicas\': 2, \'alive_replicas\': 1}')})
cqlsh:lab7r3> consistency ONE
Consistency level set to ONE.
cqlsh:lab7r3> UPDATE A SET str = 'b' WHERE id=50 IF str = 'a';
NoHostAvailable: ('Unable to complete the operation against any hosts', {<Host: 127.0.0.1:9042 datacenter1>: Unavailable('Error from server: code=1000 [Unavailable exception] message="Cannot achieve consistency level SERIAL" info={\'consistency\': \'SERIAL\', \'required_replicas\': 2, \'alive_replicas\': 1}')})
```

Тобто саме рівень реплікації 3 не дає виконати ці операції.

