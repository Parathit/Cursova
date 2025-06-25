# algorithms.py

from copy import deepcopy
from itertools import combinations


def greedy_assignment(orders, m, max_weight):
    orders = sorted(orders, key=lambda o: -o['cost'])
    assignment = {i: [] for i in range(m)}
    for order in orders:
        candidates = []
        for courier in range(m):
            weight = sum(o['weight'] for o in assignment[courier])
            if weight + order['weight'] <= max_weight:
                candidates.append(courier)
        if not candidates:
            continue
        best = min(
            candidates,
            key=lambda c: (len(assignment[c]), sum(o['cost'] * 0.2 for o in assignment[c]))
        )
        assignment[best].append(order)
    return assignment

def swap_orders(assignment, i, j, max_weight):
    for o1 in assignment[i]:
        for o2 in assignment[j]:
            w_i = sum(o['weight'] for o in assignment[i]) - o1['weight'] + o2['weight']
            w_j = sum(o['weight'] for o in assignment[j]) - o2['weight'] + o1['weight']
            if w_i <= max_weight and w_j <= max_weight:
                new_assignment = deepcopy(assignment)
                new_assignment[i].remove(o1)
                new_assignment[j].remove(o2)
                new_assignment[i].append(o2)
                new_assignment[j].append(o1)
                old_total = fairness_metrics(assignment)['order_diff'] + fairness_metrics(assignment)['reward_diff']
                new_total = fairness_metrics(new_assignment)['order_diff'] + fairness_metrics(new_assignment)['reward_diff']
                if new_total < old_total:
                    assignment[i][:] = new_assignment[i]
                    assignment[j][:] = new_assignment[j]
                    return True
    return False

def move_group_of_orders_flexible(assignment, i, j, max_weight, max_group_size=3):
    orders_i = assignment[i]
    for k in range(1, max_group_size + 1):  # групи з 1 до max_group_size
        for group in combinations(orders_i, k):
            total_weight = sum(o['weight'] for o in assignment[j]) + sum(o['weight'] for o in group)
            if total_weight <= max_weight:
                new_assignment = deepcopy(assignment)
                for o in group:
                    new_assignment[i].remove(o)
                    new_assignment[j].append(o)
                old_total = fairness_metrics(assignment)['order_diff'] + fairness_metrics(assignment)['reward_diff']
                new_total = fairness_metrics(new_assignment)['order_diff'] + fairness_metrics(new_assignment)['reward_diff']
                if new_total < old_total:
                    assignment[i][:] = new_assignment[i]
                    assignment[j][:] = new_assignment[j]
                    return True
    return False

import time

def local_search_advanced(assignment, m, max_weight, time_limit=60.0):
    start = time.time()
    while time.time() - start < time_limit:
        improved = False
        for i in range(m):
            for j in range(m):
                if i == j:
                    continue
                if swap_orders(assignment, i, j, max_weight):
                    improved = True
                    break
                if move_group_of_orders_flexible(assignment, i, j, max_weight, max_group_size=3):

                    improved = True
                    break
            if improved:
                break
        if not improved:
            break
    return assignment

def fairness_metrics(assignment):
    counts = [len(v) for v in assignment.values()]
    rewards = [sum(order['cost'] * 0.2 for order in v) for v in assignment.values()]
    return {
        'order_diff': max(counts) - min(counts),
        'reward_diff': max(rewards) - min(rewards),
        'min_orders': min(counts),
        'max_orders': max(counts),
        'min_reward': min(rewards),
        'max_reward': max(rewards)
    }

def print_assignment(assignment1, assignment2, title1="Жадібне призначення", title2="Локальне призначення"):
    header = (
        "{:^10} {:^15} {:^10} {:^15} {:^15} || {:^10} {:^15} {:^10} {:^15} {:^15}"
        .format("Кур’єр, №", "Замовлення, №", "Вага, кг", "Вартість, грн", "Премія, грн",
            "Кур’єр, №", "Замовлення, №", "Вага, кг", "Вартість, грн", "Премія, грн")
    )

    # Правильний центрований заголовок
    title_line = f" {title1}  || {title2} "
    print("=" * len(header))
    print(title_line.center(len(header), "="))
    print("=" * len(header))
    print(header)
    print("=" * len(header))

    print(header)
    print("=" * len(header))

    all_couriers = sorted(set(assignment1.keys()).union(assignment2.keys()))
    for courier in all_couriers:
        orders1 = assignment1.get(courier, [])
        orders2 = assignment2.get(courier, [])
        max_len = max(len(orders1), len(orders2))

        total1 = {"weight": 0, "cost": 0, "reward": 0}
        total2 = {"weight": 0, "cost": 0, "reward": 0}

        for i in range(max_len):
            # Ліва частина — жадібне
            if i < len(orders1):
                o1 = orders1[i]
                r1 = int(o1['cost'] * 0.2)
                row1 = [
                    f"{courier + 1}" if i == 0 else "",
                    f"{o1['id'] + 1}",
                    f"{o1['weight']}",
                    f"{o1['cost']}",
                    f"{r1}"
                ]
                total1["weight"] += o1['weight']
                total1["cost"] += o1['cost']
                total1["reward"] += r1
            else:
                row1 = [""] * 5

            # Права частина — локальне
            if i < len(orders2):
                o2 = orders2[i]
                r2 = int(o2['cost'] * 0.2)
                row2 = [
                    f"{courier + 1}" if i == 0 else "",
                    f"{o2['id'] + 1}",
                    f"{o2['weight']}",
                    f"{o2['cost']}",
                    f"{r2}"
                ]
                total2["weight"] += o2['weight']
                total2["cost"] += o2['cost']
                total2["reward"] += r2
            else:
                row2 = [""] * 5

            print("{:^10} {:^15} {:^10} {:^15} {:^15} || {:^10} {:^15} {:^10} {:^15} {:^15}".format(*row1, *row2))

        # Підсумковий рядок (Разом)
        print("{:^10} {:^15} {:^10} {:^15} {:^15} || {:^10} {:^15} {:^10} {:^15} {:^15}".format(
            "Разом", "", total1["weight"], total1["cost"], total1["reward"],
            "Разом", "", total2["weight"], total2["cost"], total2["reward"]
        ))
        print("-" * len(header))

def print_metrics_comparison(metrics1, metrics2):
    print("\n📊 Порівняння метрик справедливості:")
    print("{:<35} {:<30} {:<30}".format("Метрика", "Жадібне", "Локальне"))
    print("=" * 95)
    print("{:<35} {:<30} {:<30}".format(
        "➤ Різниця в замовленнях",
        f"{metrics1['order_diff']} (від {metrics1['min_orders']} до {metrics1['max_orders']})",
        f"{metrics2['order_diff']} (від {metrics2['min_orders']} до {metrics2['max_orders']})"
    ))
    print("{:<35} {:<30} {:<30}".format(
        "➤ Різниця в премії",
        f"{metrics1['reward_diff']:.2f} (від {metrics1['min_reward']:.2f} до {metrics1['max_reward']:.2f})",
        f"{metrics2['reward_diff']:.2f} (від {metrics2['min_reward']:.2f} до {metrics2['max_reward']:.2f})"
    ))

def solve_task(task):
    greedy = greedy_assignment(task.orders, task.num_couriers, task.max_weight)
    improved = local_search_advanced(deepcopy(greedy), task.num_couriers, task.max_weight)

    print_assignment(greedy, improved)
    print_metrics_comparison(fairness_metrics(greedy), fairness_metrics(improved))
