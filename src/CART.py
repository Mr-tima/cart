import csv
import numpy as np
from utils import get_trees

data_set = 'test'


def is_node(tree):
    if type(tree) == dict:
        return True
    return False


'''
    Проверка на чилсо
'''
def is_digit(string):
    string = str(string)
    if string.isdigit():
        return True
    else:
        try:
            float(string)
            return True
        except ValueError:
            return False


'''
    Обработка данных
'''
def processingData(data):
    survived = []
    for i in data:
        survived.append(i[1])
        del i[0:2], i[1:3], i[5], i[6]
    return data, survived


def processingTest(data):
    survived = []
    for i in data:
        survived.append(i[3])
        del i[3]
    return data, survived


def comparision(condition, att, x):
    if condition == "=":
        return x == att
    elif condition == "!=":
        return x != att
    elif condition == ">":
        return float(att) > float(x)
    elif condition == "<":
        return float(att) < float(x)
    else:
        return False


def set_count_base_class(tmp):
    res = ''
    for i in set(tmp):
        res += str(tmp.count(i))
    return res


def check(_set):
    if len(set(_set)) > 1:
        return True
    else:
        return False


def gini(T):
    result = 0
    for i in set(T):
        count = 0
        for j in T:
            if i == j:
                count += 1
        result -= (count / len(T)) ** 2
    return 1 + result


def gini_split(left, right):
    return len(left) / (len(left) + len(right)) * gini(left) + len(right) / (len(left) + len(right)) * gini(right)


def gini_split_for_category(data, base):
    res = []
    data_set = set(data)
    for i in data_set:
        left = []
        right = []
        for j in range(len(data)):
            if i == data[j]:
                left.append(base[j])
            else:
                right.append(base[j])
        res.append([i, gini_split(left, right)])
    return min(res, key=lambda x: x[1])


def gini_split_for_number(data, base):
    res = []
    data_set_sort = sorted(list(set(data)), key=lambda i: i)
    data_average = []
    for i in range(1, len(data_set_sort)):
        data_average.append((float(data_set_sort[i - 1]) + float(data_set_sort[i])) / 2)
    for i in data_average:
        left = []
        right = []
        for j in range(len(data)):
            if i < float(data[j]):
                left.append(base[j])
            else:
                right.append(base[j])
        res.append([i, gini_split(left, right)])
    return min(res, key=lambda x: x[1])


def split(data, base_prop):
    res = []
    for i in range(len(data[0])):
        if is_digit(str(np.array(data)[0, i])):
            res.append([i, gini_split_for_number(np.array(data)[0:, i], base_prop.copy())])
        else:
            res.append([i, gini_split_for_category(np.array(data)[0:, i], base_prop.copy())])
    return res


def CART(data, base_prop):
    if check(base_prop):
        tree = dict()
        result_gini = split(data, base_prop.copy())
        split_attribute = min(result_gini, key=lambda i: i[1][1])
        value_base_prop = list(set(base_prop))
        value_base_prop.sort()
        extra_data = ' {}={} {}={}'.format(value_base_prop[0], base_prop.count(value_base_prop[0]), value_base_prop[1], base_prop.count(value_base_prop[1]))
        if is_digit(split_attribute[1][0]):
            for k in range(2):
                tempData = []
                tempClass = []
                if k == 0:
                    for i in range(len(data)):
                        if float(data[i][int(split_attribute[0])]) < float(split_attribute[1][0]):
                            tempData.append(data[i])
                            tempClass.append(base_prop[i])
                    tree[str(split_attribute[0]) + " < " + str(split_attribute[1][0]) + " " + str(len(base_prop)) + extra_data] = CART(tempData, tempClass)
                else:
                    for i in range(len(data)):
                        if float(data[i][int(split_attribute[0])]) > float(split_attribute[1][0]):
                            tempData.append(data[i])
                            tempClass.append(base_prop[i])
                    tree[str(split_attribute[0]) + " > " + str(split_attribute[1][0]) + " " + str(len(base_prop)) + extra_data] = CART(tempData, tempClass)
        else:
            for k in range(2):
                tempData = []
                tempClass = []
                if k == 0:
                    for i in range(len(data)):
                        if split_attribute[1][0] == data[i][int(split_attribute[0])]:
                            tempData.append(data[i])
                            tempClass.append(base_prop[i])
                    tree[str(split_attribute[0]) + " = " + str(split_attribute[1][0]) + " " + str(len(base_prop)) + extra_data] = CART(tempData, tempClass)
                else:
                    for i in range(len(data)):
                        if split_attribute[1][0] != data[i][int(split_attribute[0])]:
                            tempData.append(data[i])
                            tempClass.append(base_prop[i])
                    tree[str(split_attribute[0]) + " != " + str(split_attribute[1][0]) + " " + str(len(base_prop)) + extra_data] = CART(tempData, tempClass)
        return tree
    else:
        return '{}={}'.format(base_prop[0], base_prop.count(base_prop[0]))


def run(tree, test):
    if type(tree) == dict:
        for i in tree.keys():
            index, action, att, count, f_class, s_class = i.split()
            if comparision(action, test[int(index)], att):
                run(tree[i], test)
    else:
        print(tree)


def add_data_to_answer(answer, value_classes):
    att, count = answer.split('=')
    new_att = None
    for i in value_classes:
        if att != i:
            new_att = i
    return '{} {}={}'.format(answer, new_att, 0)


def simplification_node_tree(tree, count):
    index, type_sign, attribute, all_example, first_class, second_class = list(tree)[0].split()
    all_example = count
    if type_sign == '=' or type_sign == '!=':
        new_sign = 'w'
    else:
        new_sign = 'n'
    return '{} {} {} {} {} {}'.format(index, new_sign, attribute, all_example, first_class, second_class)


def new_format_tree_node(tree, all_example, value_classes, new_tree=None):
    if new_tree is None:
        new_tree = {}
    if is_node(tree):
        new_branches = []
        key = simplification_node_tree(tree, all_example)
        for i in tree.keys():
            if not is_node(tree[i]):
                new_branches.append(add_data_to_answer(tree[i], value_classes))
            else:
                new_branches.append(simplification_node_tree(tree[i],all_example))
        new_tree[key] = new_branches
        for i in tree.keys():
            new_tree = new_format_tree_node(tree[i], all_example, value_classes,new_tree)
    return new_tree


def run_for_new_format_tree(tree, test):
    key = list(tree)[0]
    while True:
        index, type_sign, attribute, all_example, first_class, second_class = key.split()
        if type_sign == 'w':
            if test[int(index)] == attribute:
                if tree[key][0] in tree.keys():
                    key = tree[key][0]
                else:
                    print(tree[key][0])
                    break
            else:
                if tree[key][1] in tree.keys():
                    key = tree[key][1]
                else:
                    print(tree[key][1])
                    break
        else:
            if float(test[int(index)]) < float(attribute):
                if tree[key][0] in tree.keys():
                    key = tree[key][0]
                else:
                    print(tree[key][0])
                    break
            else:
                if tree[key][1] in tree.keys():
                    key = tree[key][1]
                else:
                    print(tree[key][1])
                    break


def main():
    path = '../resources/{}.csv'.format(data_set)
    data = []
    with open(path, 'r') as file:
        reader = csv.reader(file, delimiter=',')
        for row in reader:
            data.append(row)
    # data, base_property = processingData(data)
    data, base_property = processingTest(data)

    tree = (CART(data.copy(), base_property.copy()))
    print('Исходное дерево, построенное с использованием алгоритма CART:')
    print(tree, '\n')

    new_tree = new_format_tree_node(tree, len(base_property), set(base_property))
    print('Список деревьев, полученных после стрижки исходного:')
    get_trees(new_tree)

    print('Тестирование:', '\n', '[c, 80, Yes]')
    test = ["c", "80", "Yes"]
    run(tree, test)

    stop = input('Enter для выхода')


if __name__ == '__main__':
    main()
