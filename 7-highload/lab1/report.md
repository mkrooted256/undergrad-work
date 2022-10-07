# 7-Highload. Lab 1
Mykhailo Koreshkov, FI-91

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
> 20000

I had a lot of problems with this task.   
- first launch of 10 threads x 10000 iterations took more than 2 hours to finish and resulted in an incorrect sum (less than 20000)
- 2 threads, 1 node:
    ```
    Task '2. Pessimistic blocking' finished!
    > Result =  13673
    > Time = 6.33956s
    ```
- 2 threads, 3 nodes: 
    ```
    Task '2. Pessimistic blocking' finished!
    > Result =  19759
    > Time = 9.4751s
    ```
- more than 2 runners lead to dramatic increase in execution time so I never waited for it to finish
- I also tried to test the impact of thread.wait, but did not found any pattern 


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
