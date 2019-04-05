def handle_numbers(num1, num2, num3):
    if num3 == 0:
        return 0
    counter = 0
    for item in range(num1, num2 + 1):
        if not item % num3:
            counter += 1
    return counter


def handle_string(value):
    letters, digits = 0, 0
    for item in value:
        if item.isalpha():
            letters += 1
        elif item.isdigit():
            digits += 1
    return letters, digits


def sort(par):
    return par[0], int(par[1]), -int(par[2]), int(par[3])


def handle_list_of_tuples(list):
    return sorted(list, key=sort)


def main():
    print("handle numbers = ", handle_numbers(-21, 10, 5))
    l, d = handle_string('Hello world! 123!')
    print('letters = ', l, ', digits = ', d)
    list = [
        ("Tom", "19", "167", "54"),
        ("Jony", "24", "180", "69"),
        ("Json", "21", "185", "75"),
        ("John", "27", "190", "87"),
        ("Jony", "24", "191", "98"),
    ]
    print(handle_list_of_tuples(list))


if __name__ == '__main__':
    main()
