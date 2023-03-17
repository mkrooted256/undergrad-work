# 8-Blockchain. Lab2
Варіант 8

Михайло Корешков, ФІ-91

---

**Мета роботи:** Дослiдження особливостей блокчейн-платформи з вiдкритим кодом NaiveCoin.

---

## Вступ
Робота матиме декілька частин: практичну та теоретичну. В практичній частині я займатимуся запуском та дослідженням особливостей платформи NaiveCoin з використанням віртуальних машин (контейнерів) Docker. У якості умовного плану роботи візьму матеріал https://lhartikk.github.io/ від автора платформи.   В теоретичній частині я проведу аналіз отриманої криптовалюти: опишу використаний протокол, умови консенсусу, формат блоків, транзакцій та адрес; а також проведу базові обрахунки щодо стійкості до деяких атак.

## Практична частина

### 1. Огляд платформи
*NaiveCoin* - це платформа для створення простого розподіленого (на декілька комп'ютерів-нод) блокчейну із підтримкою функціоналу криптовалюти. Криптовалютний функціонал полягає у тому, що платформа підтримує протокол proof of work та має все необхідне для створення нових коінів та роботи з транзакціями. 

Платформа реалізована як typescript скрипт. Щоб створити ноду розподіленого блокчейну необхідно запустити цей скрипт на ноді. Після запуску нода матиме два сервіси: порт для пірингового зв'язку З іншими нодами за протоколом WebSocket та HTTP сервер для керування.
- Під піринговим зв'язком або p2p тут мається на увазі  що зацікавлені ноди спілкуватимуться між собою напряму, без центрального серверу. З цього випливатиме необхідність для кожної ноди зазначити список інших нод вручну.
- Сервер для керування дає адміністратору ноди доступ до її статусу, деталей її копії блокчейну, до додавання транзакцій та ручного запуску генерації (майнінгу) нового блоку

### 2. Встановлення та запуск
Я створив форк GitHub репозиторію https://github.com/lhartikk/naivecoin з вихідним кодом платформи (доступний за посиланням https://github.com/mkrooted256/naivecoin-term8) та завантажив його собі на комп'ютер.

Далі створив файл `Dockerfile` із специфікаціями контейнера, що мітитиме ноду, та файл `docker-compose.yml` із правилом запуску всієї мережі з декількох нод в контейнерах.
Також знадобилося змінити конфігурацію typescript.

Мережа складатиметься з 3 нод, з'єднаних послідовно (3-2, 2-1). **TODO: спробувати інші топології?**

Запускаємо 

![Alt text](imgs/1.png)  
...  
![Alt text](imgs/2.png)  
...  
![Alt text](imgs/3.png)  

- Перший запит. Об'єднання нод в мережу
    ![Alt text](imgs/req2.1.png) ![Alt text](imgs/req2.2.png)  
    ![Alt text](imgs/req2.3.png)

- Другий запит. Стан блокчейну
    ![Alt text](imgs/4.png)

- За спроби провести транзакцію нода вивела помилку, бо перша транзакція має бути створенням нових коінів:  
    ![Alt text](imgs/req3.png)  
    ![Alt text](imgs/req3.1.png)

- Збережемо адреси гаманців нод:  
    ![Alt text](imgs/addr1.png)...
    ```
    node1: 04e22af4bd3f0a6d9eadbabf6f39560935414a6a01be5f88935bda4a848a60cc61616d96b1fff0681f7892995e747bac02ffd5a904055a33ef58080bf792937eeb
    node2: 04f13d7d2aa71235ca87869b68c01099a514f455de46e6774f25add6a311380e2a2b080551bfa21e96726263f8d7330d3d7e980bd12143037e49075eec7e4f9e1a
    node3: 0497baeb849e983d6f4a9bcd5cca58a0e900745ffcbf7925da8d20ec745e71461e8a20ef1a5f27fcbe7f394ef0bc6795619beb9b94d090d5b1748c641572404d26
    ```

    Також бачимо, що всі гаманці порожні  
    ![Alt text](imgs/addr2.png)

    А список my unspent transaction output порожній  
    ![Alt text](imgs/req4.0.png)

### 3. Проведення транзакцій
- Проводимо coinbase транзакцію на першій ноді
    ![Alt text](imgs/req4.1.png)  
    Бачимо, що баланс першого гаманця збільшився  
    ![Alt text](imgs/req4.2.png)  
    А також з'явилася unspent transaction
    ![Alt text](imgs/req4.3.png)  
    Також перевіримо стан блокчейну на інших нодах:
    ![Alt text](imgs/req4.4.png)  
    Бачимо, що зміни поширились з першої на всі ноди.

- Транзакція з першої на другу ноди.  
    ![Alt text](imgs/req5.png)  

    Звернемо увагу на деікілька речей (тут і далі "коін" це синонім для unspent transaction output або просто для транзакції).
    1. Бачимо класичну модель транзакції: декілька вхідних коінів та декілька вихідних. Вихідних коінів завжди не більше двох. Вхідні коіни "знищуються", один вихідний коін йде адресату, а інший - це "решта", що повертається відправнику.
    2. Список блоків та баланси гаманців не змінилися, бо транзакція ще не потрапила в жоден блок
    3. Транзакція потрапила в загальний для всіх нод пул транзакцій  
        ![Alt text](imgs/req5.1.png)

- Майнимо блок на першій ноді.  
    Бачимо, що блок поширився на всі ноди.  
    ![Alt text](imgs/req6.1.png)  
    А також бачимо, що зміни в балансах застосувалися.  
    ![Alt text](imgs/req6.2.png) ![Alt text](imgs/req6.3.png)

- Надішлемо 60 коінів третій ноді, щоб продемонструвати об'єднання коінів  
    ![Alt text](imgs/req7.1.png)  
    Проаналізуємо вхідні коіни (TxIns)
    1. 50 взято з першого (та єдиного) виходу coinbase транзакції, змайненої на першій ноді ![Alt text](imgs/req7.2.png)
    2. 10 взято з другого виходу попередної транзакції ![Alt text](imgs/req7.3.png)

### 4. Реакція на зловмисну ноду
- Надішлемо 1000 коінів з першої на другу ноду, щоб продемонструвати відхилення невалідної транзакції  
    Спочатку я додам транзакцію у пул з першої ноди, а потім змайню іншою (третьою) нодою.  
    Оскільки ноди реалізовані чесно, то операція провалилась ще на етапі створення транзакції.  
    ![Alt text](imgs/req8.0.png)  
    Тому я відредагував код та додав опцію "malicious", яка обійде всі перевірки для операції. Спробуємо ще раз  

    > Хочу наголосити, що тут мені знадобилося перезавантажити першу ноду. Після запуску та додавання адреси інших нод вона автоматично відновила блокчейн та свій актуальний баланс за інформацією від них.

    > Нова адреса першої ноди `0493f47b2523cc03bfdfa0f717c654295d030a3ba4cea379445bb5415497f9da69a8de95e208922fdc2d90e7100a5a767d22002ac2a6d3e51c01a3dbd4c3478cd5`

    ![Alt text](imgs/req8.1.png)
    ![Alt text](imgs/req8.3.png)
    ![Alt text](imgs/req8.4.png)

    Транзакція залишилась в transaction pool лише зловмисної ноди, всі інші відкинули її.

- Спробуємо змайнити блок на зловмисній ноді та подивимося на реакцію інших нод.  

    Спостерігаємо відкидання опублікованого блоку
    ![Alt text](imgs/req8.5.png)

    А також розбіжності в стані блокчейну для різних нод:
    ![Alt text](imgs/req8.6.png) та ![Alt text](imgs/req8.7.png)

### 5. Атака подвійної витрати
План виконання атаки наступний:
1. транзакція з першої на другу ноду 
2. роз'єднати мережеве з'єднання між нодами
3. змайнити блок з цією транзакцією на третій ноді
4. очистити пул транзакцій на першій ноді
5. змайнити два блоки на першій ноді
6. відновити з'єднання між нодами

В результаті друга та третя ноди мають замінити свій блокчейн тим, що пропонує перша нода.

> Для виконання цієї атаки необхідно реалізувати функцію ручного очищення пулу транзакцій

> нова адреса першої ноди `044a100e7fba65b6b14b19dfa18f8ca8bea5711038e107862802d924a85f2158c02c8ab4407167f8af2c5b77d05195f832d5353822b3b590e39e5c3584e88e7c98`

Роз'єднання зв'язку виконуватиму командою `docker network disconnect naivecoin_coin naivecoin-node1-1`.

1. транзакція з першої на другу ноду ![Alt text](imgs/ds1.png)
2. роз'єднати мережеве з'єднання між нодами  
    ```
    docker network disconnect naivecoin_coin naivecoin-node1-1
    docker network connect bridge naivecoin-node1-1
    ```.  
    ![Alt text](imgs/ds2.png)
3. змайнити блок з цією транзакцією на третій ноді ![Alt text](imgs/ds3.png)
4. очистити пул транзакцій на першій ноді  ![Alt text](imgs/ds4.png)
5. змайнити два блоки на першій ноді  ![Alt text](imgs/ds5.1.png) ![Alt text](imgs/ds5.2.png)
6. відновити з'єднання між нодами  
    `docker network connect naivecoin_coin naivecoin-node1-1`  
    Але спочатку подивимося стан блокчейну з точки зору різних нод:
    1. нода 1  
        ![Alt text](imgs/ds6.1.png)
    2. нода 2  
        ![Alt text](imgs/ds6.2.png)
    3. нода 3  
        ![Alt text](imgs/ds6.3.png)
7. результат  
    ![Alt text](imgs/ds7.png)  
    1. нода 1  
        ![Alt text](imgs/ds6.1.png)
    2. нода 2  
        ![Alt text](imgs/ds7.2.png)
    3. нода 3  
        ![Alt text](imgs/ds7.3.png)
    
Отже, атака успішло виконана.

## Теоретична частина

Блокчейн починається генезис блоком. У ньому для нас найголовніше - параметри.

Основні параметри, які нас цікавлять, це бажана часова складність криптовалюти та частота оновлення параметра складності. Параметр складності (`difficulty` у списку блоків) задає скільки нулів на початку хеша має мати блок. Для підбору хеша майнер не може змінювати дані, але може спеціальне поле `nonce`.

Складність зростатиме якщо блоки створюються занадто швидко. Наприклад:

![Alt text](imgs/req10.png)

Тут видно в тому числі що за нульової складності `nonce` залишається нульовим.

