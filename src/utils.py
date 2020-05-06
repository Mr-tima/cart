import copy


def cutting(tree, nodes):
    for i in nodes:
        del tree[i]
    return tree


def errors_all_sheets_subtree(tree, node, set_errors_value=None):
    if set_errors_value is None:
        set_errors_value = []
    subtree = tree[node]
    for i in subtree:
        if not (i in tree.keys()):
            first_class, second_class = i.split()
            set_errors_value.append(min(int(first_class.split('=')[1]), int(second_class.split('=')[1])))
        else:
            set_errors_value = errors_all_sheets_subtree(tree, i, set_errors_value)
    return set_errors_value


def cut_tree(tree):
    set_lambdas = {}
    min_lambda = None
    for i in tree.keys():
        index, operation, split_attribute, all_example, first_class, second_class = i.split()
        first_class, second_class = first_class.split('=')[1], second_class.split('=')[1]
        error_classification = min(int(first_class), int(second_class)) / int(all_example)
        set_values_error_in_sheets = errors_all_sheets_subtree(tree, i)
        sum_errors_all_sheets = sum(i / int(all_example) for i in set_values_error_in_sheets)
        set_lambdas[i] = (error_classification - sum_errors_all_sheets) / (len(set_values_error_in_sheets) - 1)
        min_lambda = min(set_lambdas.values())
    set_min_connections = [k for k, v in set_lambdas.items() if v == min_lambda]
    if list(tree)[0] in set_min_connections:
        return ['{}'.format(list(tree)[0].split()[4]), '{}'.format(list(tree)[0].split()[5])]
    for i in set_min_connections:
        for val in tree.values():
            if i in val:
                if i == val[0]:
                    new_sheets = '{} {}'.format(i.split()[4], i.split()[5])
                    val[0] = new_sheets
                else:
                    new_sheets = '{} {}'.format(i.split()[4], i.split()[5])
                    val[1] = new_sheets
    tree = cutting(tree, set_min_connections)
    # print(tree)
    return tree


def get_trees(tree):
    trees = [copy.deepcopy(tree)]
    while True:
        tree = cut_tree(copy.deepcopy(tree))
        if type(tree) != dict:
            trees.append(tree)
            break
        trees.append(tree)
    list(map(print, trees))
    print()


def main():
    tree = {'0 w b 200 +=100 -=100': ['0 w b 200 +=90 -=60', '0 w b 200 +=10 -=40'],
            '0 w b 200 +=90 -=60': ['+=80 -=0', '0 w b 200 +=10 -=60'],
            '0 w b 200 +=10 -=60': ['+=0 -=60', '+=10 -=0'],
            '0 w b 200 +=10 -=40': ['+=10 -=0', '+=0 -=40']}

    get_trees(tree)


if __name__ == '__main__':
    main()
