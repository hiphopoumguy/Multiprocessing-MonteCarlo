import random
import time
from multiprocessing import Pool, current_process
import matplotlib.pyplot as plt

def tic():
    global start_time
    start_time = time.time()

def toc(tag="elapsed time"):
    if "start_time" in globals():
        return time.time() - start_time
    else:
        print("tic has not been called")

# モンテカルロ法によるπの計算
def calc_pi(sim_num):
    # 各プロセスで異なるシードを設定
    random.seed(current_process().pid)
    
    inside_cnt = 0
    for _ in range(sim_num):
        x = random.random()
        y = random.random()
        d = (x**2) + (y**2) # math.sqrt((x-0)**2 + (y-0)**2) 
        
        if d <= 1:
            inside_cnt += 1
    pi = inside_cnt / sim_num * 4   
    
    return pi

if __name__ == "__main__":
    sim_num = 10000000
    print('sim_num = %d' % sim_num)

    # 並列処理での計算
    core_nums = 4  # コア数
    core_counts = list(range(1, core_nums + 1))
    times = []
    core_times_product = []

    for core_num in core_counts:
        sim_num_per_worker = sim_num // core_num
        remainder = sim_num % core_num
        sim_counts = [sim_num_per_worker + 1 if i < remainder else sim_num_per_worker for i in range(core_num)]
        
        tic()
        with Pool(processes=core_num) as pool:
            results = pool.map(calc_pi, sim_counts)
        
        pi = sum(results) / core_num
        elapsed_time = toc()
        times.append(elapsed_time)
        core_times_product.append(core_num * elapsed_time)

        print(f'core_num = {core_num}')
        print(f'pi = {pi:.6f}, time = {elapsed_time:.4f}')

    # グラフの作成
    plt.figure(figsize=(10, 6))
    plt.plot(core_counts, times, marker='o', label='Execution Time')
    plt.plot(core_counts, core_times_product, marker='o', label='Core Count x Execution Time')
    plt.xlabel('Number of Cores')
    plt.ylabel('Time (seconds)')
    plt.title('Execution Time and Core Count x Execution Time vs Number of Cores')
    plt.legend()
    plt.grid(True)
    plt.show()
