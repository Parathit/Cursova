# experiments.py

import time
import matplotlib.pyplot as plt
from copy import deepcopy
from io_utils import input_random_custom, input_random
from algorithms import greedy_assignment, local_search_advanced, fairness_metrics

def experiment_t_max():
    print("\n--- Експеримент: параметр завершення роботи ---")
    t_max_values = [float(x) for x in input("Введіть список T_max (через пробіл): ").split()]
    K = int(input("Кількість повторів для кожного T_max: "))
    n = int(input("Кількість замовлень: "))
    m = int(input("Кількість кур'єрів: "))
    W = int(input("Максимальна вага для кур'єра: "))

    avg_times = []
    avg_order_diffs = []
    avg_reward_diffs = []
    for t_max in t_max_values:
        total_time = 0
        total_order_diff = 0
        total_reward_diff = 0
        for _ in range(K):
            orders = input_random(n, m, W).orders
            greedy = greedy_assignment(orders, m, W)
            start = time.time()
            improved = local_search_advanced(deepcopy(greedy), m, W, t_max)
            duration = time.time() - start
            metrics = fairness_metrics(improved)
            total_time += duration
            total_order_diff += metrics['order_diff']
            total_reward_diff += metrics['reward_diff']
        avg_times.append(total_time / K)
        avg_order_diffs.append(total_order_diff / K)
        avg_reward_diffs.append(total_reward_diff / K)
    plt.figure()
    plt.plot(t_max_values, avg_times, marker='o')
    plt.xlabel("T_max (сек)")
    plt.ylabel("Середній час виконання (сек)")
    plt.title("Час виконання від T_max")
    plt.grid()
    plt.show()
    plt.figure()
    plt.plot(t_max_values, avg_order_diffs, marker='o', label="Різниця замовлень")
    plt.plot(t_max_values, avg_reward_diffs, marker='x', label="Різниця премій")
    plt.xlabel("T_max (сек)")
    plt.ylabel("Середнє значення")
    plt.title("Справедливість від T_max")
    plt.legend()
    plt.grid()
    plt.show()

def experiment_size():
    print("\n--- Експеримент: вплив розмірності ---")
    count = int(input("Кількість конфігурацій для перевірки: "))
    sizes = []
    for _ in range(count):
        n = int(input("Кількість замовлень: "))
        m = int(input("Кількість кур'єрів: "))
        sizes.append((n, m))

    W = int(input("Максимальна вага для кур'єра: "))
    K = int(input("Кількість ІЗ (повторів) для кожної конфігурації: "))

    # ⬇️  нові масиви для часу виконання
    greedy_times, local_times = [], []

    greedy_order_diffs, local_order_diffs = [], []
    greedy_reward_diffs, local_reward_diffs = [], []

    for n, m in sizes:
        g_order_diff = l_order_diff = 0
        g_reward_diff = l_reward_diff = 0
        g_time = l_time = 0

        for _ in range(K):
            orders = input_random(n, m, W).orders

            # -- Жадібний алгоритм
            start = time.time()
            greedy = greedy_assignment(orders, m, W)
            g_time += time.time() - start

            # -- Локальний пошук
            start = time.time()
            improved = local_search_advanced(deepcopy(greedy), m, W)
            l_time += time.time() - start

            g_metrics = fairness_metrics(greedy)
            l_metrics = fairness_metrics(improved)

            g_order_diff += g_metrics['order_diff']
            l_order_diff += l_metrics['order_diff']
            g_reward_diff += g_metrics['reward_diff']
            l_reward_diff += l_metrics['reward_diff']

        # середні значення по K повторів
        greedy_order_diffs.append(g_order_diff / K)
        local_order_diffs.append(l_order_diff / K)
        greedy_reward_diffs.append(g_reward_diff / K)
        local_reward_diffs.append(l_reward_diff / K)
        greedy_times.append(g_time / K)
        local_times.append(l_time / K)


    labels = [f"{n}/{m}" for n, m in sizes]

    # --- 📈  графіки (різниця замовлень / премій) ---
    plt.figure()
    plt.plot(labels, greedy_order_diffs, marker='o', label="Жадібний: замовлення")
    plt.plot(labels, local_order_diffs, marker='x', label="Локальний: замовлення")
    plt.title("Середня різниця кількості замовлень")
    plt.grid(); plt.legend(); plt.show()

    plt.figure()
    plt.plot(labels, greedy_reward_diffs, marker='o', label="Жадібний: премія")
    plt.plot(labels, local_reward_diffs, marker='x', label="Локальний: премія")
    plt.title("Середня різниця премій")
    plt.grid(); plt.legend(); plt.show()

    # --- 🆕  Графік часу виконання ---
    plt.figure()
    plt.plot(labels, greedy_times, marker='o', label="Жадібний алгоритм")
    plt.plot(labels, local_times, marker='x', label="Локальний пошук")
    plt.title("Залежність часу виконання від розмірності")
    plt.ylabel("Середній час, с")
    plt.xlabel("n / m  (замовлення / кур'єри)")
    plt.grid(); plt.legend(); plt.show()
