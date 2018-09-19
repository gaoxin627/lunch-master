import random


def rand_restaurant(restaurant_list_file):
    restaurant_list = []
    with open(restaurant_list_file, mode="r", encoding='utf-8') as f:
        for line in f:
            restaurant_list.append(line.strip())
    i = random.randint(1, len(restaurant_list))
    return restaurant_list[i - 1]


if __name__ == "__main__":
    file = 'restaurant'
    print(rand_restaurant(file))

