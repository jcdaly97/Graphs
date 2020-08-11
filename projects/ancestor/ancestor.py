
def earliest_ancestor(ancestors, starting_node):
    dictionary = make_dictionary(ancestors)
    current_generation = []
    if starting_node not in dictionary:
        return -1
    current_generation.extend(dictionary[starting_node])
    while True:
        current_generation.sort()
        next_generation = []
        for c in current_generation:
            if c in dictionary:
                next_generation.extend(dictionary[c])
        if len(next_generation) < 1:
            return current_generation[0]
        else:
            current_generation = next_generation

def make_dictionary(arr):
    dictionary = {}
    for a in arr:
        if a[1] not in dictionary:
            dictionary[a[1]] = list()
            dictionary[a[1]].append(a[0])
        else:
            dictionary[a[1]].append(a[0])
    return dictionary


test = [(1, 3), (2, 3), (3, 6), (5, 6), (5, 7), (4, 5), (4, 8), (8, 9), (11, 8), (10, 1)]
print(make_dictionary(test))
print(earliest_ancestor(test, 6))
"""
       10
     /
    1   2   4  11
     \ /   / \ /
      3   5   8
       \ / \   \
        6   7   9
"""