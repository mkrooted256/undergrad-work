import psycopg2
import concurrent.futures
import time

connconfig = "dbname=postgres user=postgres password=helloworld"


def setup():
    conn = psycopg2.connect(connconfig)
    cur = conn.cursor()
    cur.execute("DROP TABLE if exists lab2;")
    cur.execute("CREATE TABLE lab2 (user_id serial PRIMARY KEY, counter integer, version integer);")

    cur.execute("INSERT INTO lab2 (user_id, counter, version) VALUES (%s, %s, %s);", (1, 0, 0))

    cur.execute("SELECT * FROM lab2;")
    print(cur.fetchone())

    conn.commit()

    cur.close()
    conn.close()

def worker_dumb(worker_id):
    conn = psycopg2.connect(connconfig)
    cur = conn.cursor()
    print(f"Worker {worker_id} started.")
    for i in range(10000):
        cur.execute("SELECT counter FROM lab2 WHERE user_id=1;")
        counter = cur.fetchone()[0] + 1
        cur.execute("UPDATE lab2 SET counter=%s WHERE user_id=1;", (counter,))
        conn.commit()
        if i % 1000 == 0:
            print(f"Worker {worker_id} - {i} - {counter}")
    print(f"Worker {worker_id} finished!")
    cur.close()
    conn.close()
    
def worker_inplace(worker_id):
    conn = psycopg2.connect(connconfig)
    cur = conn.cursor()
    print(f"Worker {worker_id} started.")
    for i in range(10000):
        cur.execute("UPDATE lab2 SET counter=counter+1 WHERE user_id=1;")
        conn.commit()
        if i % 1000 == 0:
            print(f"Worker {worker_id} - {i}")
    print(f"Worker {worker_id} finished!")
    cur.close()
    conn.close()

def worker_rowlock(worker_id):
    conn = psycopg2.connect(connconfig)
    cur = conn.cursor()
    print(f"Worker {worker_id} started.")
    for i in range(10000):
        cur.execute("SELECT counter FROM lab2 WHERE user_id=1 FOR UPDATE;")
        counter = cur.fetchone()[0] + 1
        cur.execute("UPDATE lab2 SET counter=%s WHERE user_id=1;", (counter,))
        conn.commit()
        if i % 1000 == 0:
            print(f"Worker {worker_id} - {i}")
    print(f"Worker {worker_id} finished!")
    cur.close()
    conn.close()
    
def worker_optimistic(worker_id):
    conn = psycopg2.connect(connconfig)
    cur = conn.cursor()
    print(f"Worker {worker_id} started.")
    for i in range(10000):
        while True:
            cur.execute("SELECT counter,version FROM lab2 WHERE user_id=1;")
            counter,version = cur.fetchone()
            cur.execute("UPDATE lab2 SET counter=%s,version=%s WHERE user_id=1 and version=%s;", 
                        (counter+1,version+1,version))
            conn.commit()
            if cur.rowcount > 0:
                break
        if i % 1000 == 0:
            print(f"Worker {worker_id} - {i}")
    print(f"Worker {worker_id} finished!")
    cur.close()
    conn.close()

def execute(title, work):
    setup()

    start = time.perf_counter_ns()
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        workers = [executor.submit(work, i) for i in range(10)]
        # concurrent.futures.wait(workers) # implicitly via 'with'
    
    delta = time.perf_counter_ns() - start

    conn = psycopg2.connect(connconfig)
    cur = conn.cursor()
    cur.execute("SELECT counter FROM lab2 WHERE user_id=1;")
    res = cur.fetchone()
    cur.close()
    conn.close()


    print(f"Task {title} - Finished")
    print(f"> Time = {delta / 1000000000:.2f}s")
    print(f"> Result = {res}")


def main():
    # execute("1. Dumb", worker_dumb)
    # execute("2. In-place update", worker_inplace)
    # execute("3. Row-level locking", worker_rowlock)
    execute("4. Optimistic locking", worker_optimistic)


if __name__ == "__main__":
    main()
