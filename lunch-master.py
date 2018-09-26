import random
import datetime
import math


MAX_HISTORY_SIZE = 5


def build_restaurants_list(restaurant_file_path):
    restaurant2id = {}
    id2restaurant = {}
    weights = []
    with open(restaurant_file_path, 'r', encoding='utf-8') as res_file:
        for (i, line) in enumerate(res_file):
            restaurant, weight = line.strip().split('@@')
            restaurant2id[restaurant] = i
            id2restaurant[i] = restaurant
            weights.append(float(weight))
    weights = [w / sum(weights) for w in weights]
    return restaurant2id, id2restaurant, weights


def adjust_weights_from_history(weights, restaurant2id, history_file_path):
    try:
        print('Before adjustment:')
        for (i, w) in enumerate(weights):
            print(f'{i}: {w}')
        today = datetime.datetime.now().date()
        adjusted_ids = set()
        surplus_weight = 0.
        with open(history_file_path, 'r', encoding='utf-8') as history_file:
            for line in history_file:
                date, restaurant = line.strip().split('@@')
                date = datetime.datetime.strptime(date, '%Y%m%d').date()
                date_delta = (today - date).days
                decay_ratio = (1. - math.exp(-date_delta)) * 0.8
                restaurant_id = restaurant2id[restaurant]
                original_weight = weights[restaurant_id]
                new_weight = original_weight * decay_ratio
                surplus_weight += (original_weight - new_weight)
                weights[restaurant_id] = new_weight
                adjusted_ids.add(restaurant_id)
        if len(adjusted_ids) == len(weights):
            num_bonus_restaurants = len(weights)
            adjusted_ids = set()
        else:
            num_bonus_restaurants = len(weights) - len(adjusted_ids)
        extra_weight_per_restaurant = surplus_weight / num_bonus_restaurants
        for i in range(len(weights)):
            if i not in adjusted_ids:
                weights[i] += extra_weight_per_restaurant
        print('After adjustment')
        for (i, w) in enumerate(weights):
            print(f'{i}: {w}')
    except FileNotFoundError:
        pass


def rand_restaurant(weights, id2restaurant, history_file_path):
    r = random.random()
    acc = 0
    final_res_id = 0
    while True:
        for i in range(len(weights)):
            acc += weights[i]
            if acc > r:
                final_res_id = i
                break
        restaurant_name = id2restaurant[final_res_id]
        print(restaurant_name + ' , accept? Press n to random again, any other key to accept')
        feedback = input()
        if feedback.lower() != 'n':
            today_str = datetime.datetime.strftime(datetime.datetime.today(), '%Y%m%d')
            try:
                with open(history_file_path, 'r', encoding='utf-8') as history_file:
                    histories = history_file.readlines()
                if len(histories) >= MAX_HISTORY_SIZE:
                    histories = [today_str + '@@' + restaurant_name + '\n'] + histories[:MAX_HISTORY_SIZE - 1]
                else:
                    histories = [today_str + '@@' + restaurant_name + '\n'] + histories
            except FileNotFoundError:
                histories = [today_str + '@@' + restaurant_name + '\n']
            with open(history_file_path, 'w+', encoding='utf-8') as history_file:
                history_file.writelines(histories)
            break


def main():
    res_file = 'restaurant'
    his_file = 'history'
    restaurant2id, id2restaurant, weights = build_restaurants_list(res_file)
    adjust_weights_from_history(weights, restaurant2id, his_file)
    rand_restaurant(weights, id2restaurant, his_file)


if __name__ == "__main__":
    main()
