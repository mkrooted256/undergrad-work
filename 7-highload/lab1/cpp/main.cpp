#include <hazelcast/client/hazelcast.h>
#include <thread>
#include <iostream>
#include <chrono>

using namespace hazelcast::client;

#define CLUSTER_IP "172.18.0.2"

// Dumb increment with race conditions
void task_dumb(int worker_num)
{
    client_config config;
    config.set_cluster_name("dev");
    config.get_network_config().add_address(address(CLUSTER_IP, 5701));
    auto hz = hazelcast::new_client(std::move(config)).get();
    auto map = hz.get_map( "map" ).get();
    const std::string key("1");
    
    std::cout << "Starting worker " << worker_num << std::endl;
    for (int k = 0;k < 10000; ++k) {
        try {
            int value = map->get<std::string, int>(key).get().value_or(0);
            map->put(key, value+1).get();
        } catch (...) {
            std::cout << "exception in incr";
        }
        if (k % 1000 == 0) std::cout << "Worker " << worker_num << " - " << k << std::endl;
    }
    std::cout << "Worker " << worker_num << " finished!" << std::endl;
}

void task_pessimistic(int worker_num)
{
    client_config config;
    config.set_cluster_name("dev");
    config.get_network_config().add_address(address(CLUSTER_IP, 5701));
    auto hz = hazelcast::new_client(std::move(config)).get();
    auto map = hz.get_map( "map" ).get();
    const std::string key("1");
    
    std::cout << "Starting worker " << worker_num << std::endl;
    int value = -1;
    for (int k = 0;k < 10000; ++k) {
        // std::cout << "L" << worker_num << std::endl;
        map->lock(key).get(); // pessimistic locking here
        try {
            value = map->get<std::string, int>(key).get().value_or(0);
            map->put<std::string, int>(key, value+1).get();
        } catch (...) {
            std::cout << "exception in incr";
        }
        map->unlock(key).get();
        // std::cout << "U" << worker_num << std::endl;
        if (k % 10 == 0) std::cout << "Worker " << worker_num << " - " << k << " - v" << value << std::endl;
    }
    std::cout << "Worker " << worker_num << " finished!" << std::endl;
}
void task_optimistic(int worker_num)
{
    client_config config;
    config.set_cluster_name("dev");
    config.get_network_config().add_address(address(CLUSTER_IP, 5701));
    auto hz = hazelcast::new_client(std::move(config)).get();
    auto map = hz.get_map( "map" ).get();
    const std::string key("1");
    
    std::cout << "Starting worker " << worker_num << std::endl;
    for (int k = 0;k < 10000; ++k) {
        while (true)
        {
            int old_value = map->get<std::string, int>(key).get().value_or(0);
            int new_value = old_value + 1;
            if (map->replace(key, old_value, new_value).get())
                break;
        }
        if (k % 1000 == 0) std::cout << "Worker " << worker_num << " - " << k << std::endl;
    }
    std::cout << "Worker " << worker_num << " finished!" << std::endl;
}

void task_cp_atomic(int worker_num)
{
    client_config config;
    config.set_cluster_name("dev");
    config.get_network_config().add_address(address(CLUSTER_IP, 5701));
    auto hz = hazelcast::new_client(std::move(config)).get();
    auto cp_subsystem = hz.get_cp_subsystem();
    
    std::cout << "Starting worker " << worker_num << std::endl;
    for (int k = 0;k < 10000; ++k) {
        auto atomic_counter = cp_subsystem.get_atomic_long("counter").get();
        atomic_counter->add_and_get(1).get();
        if (k % 1000 == 0) std::cout << "Worker " << worker_num << " - " << k << std::endl;
    }
    std::cout << "Worker " << worker_num << " finished!" << std::endl;
}

void execute_task(std::string task_name, int workers, void task(int), bool atomic = false)
{
    // definitions to measure execution time
    using std::chrono::high_resolution_clock;
    using std::chrono::duration_cast;
    using std::chrono::duration;
    using std::chrono::milliseconds;
    using std::chrono::seconds;
    
    // Init counter with 0
    client_config config;
    config.get_network_config().add_address(address(CLUSTER_IP, 5701));
    config.set_cluster_name("dev");
    auto hz = hazelcast::new_client(std::move(config)).get();
    auto map = hz.get_map( "map" ).get();
    const std::string key("1");

    if (atomic)
    {
        hz.get_cp_subsystem().get_atomic_long("counter").get()->set(0).get();
    } else
    {
        map->put<std::string, int>(key, 0).get();
        int res = map->get<std::string, int>(key).get().value();
        std::cout << "init'ed map.1 with value " << res;
    }

    // Start threads
    std::vector<std::thread> threads;
    std::cout << "Starting task '" << task_name << "'" << std::endl;

    auto t1 = high_resolution_clock::now();
    
    for (int k = 0;k < workers; ++k) {
        threads.push_back(std::thread(task, k));
    }

    for (auto &th : threads) {
        th.join();
    }

    auto t2 = high_resolution_clock::now();
    
    std::cout << std::endl << "Task '" << task_name << "' finished!" << std::endl;
    if (atomic)
    {
        long long val = hz.get_cp_subsystem().get_atomic_long("counter").get().get()->get().get();
        std::cout << "> Result (atomic long) = " << val << std::endl;
    } else
    {
        std::cout << "> Result = " << map->get<std::string, int>(key).get() << std::endl;
    }
    std::cout << "> Time = " << duration_cast<std::chrono::duration<float>>(t2 - t1).count() << "s" << std::endl << std::endl;
}

int main(int argc, char** argv) {
    int task = 0;
    if (argc > 1) {
        task = std::atoi(argv[1]);
        if (task < 1 || task > 5) {
            std::cout << "invalid task number. supported tasks: 1,2,3,4 and 5 for all. Aborting";
            return 1;
        }
    }

    // Tasks 1-3
    if(task==1 || task==5) execute_task("1. Simple increment", 10, task_dumb);
    if(task==2|| task==5) execute_task("2. Pessimistic blocking", 10, task_pessimistic);
    if(task==3|| task==5) execute_task("3. Optimistic blocking", 10, task_optimistic);

    // Task 4 - launched separately on a different set of hazelcast nodes
    if(task==4|| task==5) execute_task("4. IAtomicLong", 10, task_cp_atomic, true);

    
    return 0;
}
