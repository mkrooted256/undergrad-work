# 7-Highload. Lab 1
Mykhailo Koreshkov, FI-91

__updated on 14.12.2022__

## Task 1. No locking
10 concurrent clients incrementing counter in a Distributed Map 10000 times each.

Expected result:
> 100000

Actual result:
- 1 node
    ```
    Task '1. Simple increment' finished!
    > Result =  17141
    > Time = 9.15453s
    ```
- 3 nodes
    ```
    Task '1. Simple increment' finished!
    > Result =  18817
    > Time = 10.1101s
    ```


## Task 2. Pessimistic locking
Same, but with `map.lock`

Expected result:
> 100000

I had a lot of problems with this task because I forgot to `.get` the `map.lock()`. 
But here are the final results:

- 10 threads, 3 nodes: 
    ```
    Task '2. Pessimistic blocking' finished!
	> Result =  100000
	> Time = 161.528s
    ```



## Task 3. Optimistic locking
Same, but with optimistic locking

Expected result:
> 100000

Actual result:
- 1 node
    ```
    Task '3. Optimistic blocking' finished!
    > Result =  100000
    > Time = 34.4809s
    ```
- 3 nodes
    ```
    Task '3. Optimistic blocking' finished!
    > Result =  100000
    > Time = 41.617s
    ```

## Task 4. IAtomicLong and CP Susbsystem
> This task performed on a different set of hazelcast nodes with enabled cp-subsystem

Expected result:
> 100000

Actual result (only 3 nodes):
```
Task '4. IAtomicLong' finished!
> Result (atomic long) = 100000
> Time = 16.7404s
```

## Висновки
- "З великим конкаренсі приходить велика відповідальність"
- Налаштовувати мережевий зв'язок між хост-системою та контейнерами буває складно. В результаті я упакував виконуваний файл в інший контейнер.
- Песимістичне блокування працює дуже повільно
- Оптимістичне блокування працює на подив чудово та швидко
- Менше інстансів бази даних - швидше
- Атомні операції це класно

