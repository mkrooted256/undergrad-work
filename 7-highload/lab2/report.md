# 7-Highload. Lab 2
Mykhailo Koreshkov, FI-91

## Setup

- один докер контейнер з postgresql
- клієнт у вмгляді python скрипта

## Task 1. Lost-update (no locking)
Expected result - 100000

Actual result:
```
Task 1. Dumb - Finished
> Time = 469.01s
> Result = (10002,)
```

Note: The actual result is *10_000* instead of expected *100_000*

## Task 2. In-place update (db-managed locking)
Expected result - 100000

Actual result:
```
Task 2. In-place update - Finished
> Time = 468.64s
> Result = (100000,)
```

## Task 3. Row-level locking (manual locking)
Expected result - 100000

Actual result:
```
Task 3. Row-level locking - Finished
> Time = 584.85s
> Result = (100000,)
```

## Task 4. Optimistic locking

- Expected 10x1000=10000. Actual:
    ```
    Task 4. Optimistic locking - Finished
    > Time = 350.17s
    > Result = (10000,)
    ```
- Expected 10x10000=100000. Actual:
    ```
    Task 4. Optimistic locking - Finished
    > Time = 3927.65s
    > Result = (100000,)
    ```   
    Маємо колосальний час виконання.





