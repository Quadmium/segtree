# Idan Raiter June 5
import random
import math

def rand_list(n, biggest):
    return [int(biggest*random.random()) for i in range(n)]

def gen_tree(data):
    n = len(data)
    # At most ceil(log_k(n)) levels
    num_levels = math.ceil(math.log(n, k))
    # Infinite series sum of upper bound on # of elements in each layer
    # We can either complete n/k groups or have one group left over
    # Complete:  n/k + n/k^2 + n/k^3 + ... = n / (k-1)
    # Left over: 1 + 1 + ... log_k(n) times = log_k(n) = num_levels
    seg_size = n // (k-1) + num_levels
    seg = [0] * seg_size
    # (level start idx, num elements)
    level_ptrs = [(-1, 0)] * num_levels
    level = 0
    seg_ptr = 0
    # Bottom level starts at 0
    level_ptrs[0] = (0, -1)
    # While last generated level is not the root, generate more
    while level == 0 or level_ptrs[level-1][1] != 1:
        initial_seg_ptr = seg_ptr
        level_elements = 0
        if level == 0:
            for i in range(0, len(data), k):
                max_val = 0
                for c in range(i, min(i+k, len(data))):
                    max_val = max(max_val, data[c])
                seg[seg_ptr] = max_val
                seg_ptr += 1
                level_elements += 1
        else:
            last_level_ptr, num_last_level = level_ptrs[level-1]
            for i in range(last_level_ptr, last_level_ptr + num_last_level, k):
                max_val = 0
                for c in range(i, min(i+k, last_level_ptr + num_last_level)):
                    max_val = max(max_val, seg[c])
                seg[seg_ptr] = max_val
                seg_ptr += 1
                level_elements += 1
        level_ptrs[level] = (initial_seg_ptr, level_elements)
        level += 1
    return seg, level_ptrs

def query(left, right, seg, level_ptrs, data):
    n = len(data)
    m = max(data[left], data[right])
    parent_left = left // k
    parent_right = right // k
    child_p_left = left // k * k
    child_p_right = right // k * k
    left_idx = left - child_p_left
    right_idx = right - child_p_right
    children_left = k if parent_left < n // k else (len(data) - n // k * k)
    children_right = k if parent_right < n // k else (len(data) - n // k * k)
    if parent_left == parent_right:
        return max(data[left:right+1])
    if left_idx != 0:
        for i in range(left, child_p_left + children_left):
            m = max(m, data[i])
        left = (child_p_left + children_left) // k
    else:
        left = left // k
    if right_idx != k-1:
        for i in range(child_p_right, right+1):
            m = max(m, data[i])
        right = (child_p_right - 1) // k
    else:
        right = right // k
    level = 0
    level_ptr = level_ptrs[level][0]
    next_level_ptr = level_ptrs[level+1][0]
    while (left - level_ptr) // k != (right - level_ptr) // k and left < right:
        #print("max: {}, left: {}, right: {}".format(m, left, right))
        m = max(m, seg[left])
        m = max(m, seg[right])
        level_ptr = level_ptrs[level][0]
        num_elements = level_ptrs[level][1]
        parent_left = next_level_ptr + (left - level_ptr) // k
        parent_right = next_level_ptr + (right - level_ptr) // k
        child_p_left = level_ptr + (parent_left - next_level_ptr) * k
        child_p_right = level_ptr + (parent_right - next_level_ptr) * k
        left_idx = left - child_p_left
        right_idx = right - child_p_right
        children_left = k if (parent_left - next_level_ptr) < num_elements // k else (num_elements - num_elements // k * k)
        children_right = k if (parent_left - next_level_ptr) < num_elements // k else (num_elements - num_elements // k * k)
        if left_idx != 0:
            for i in range(left, child_p_left + children_left):
                m = max(m, seg[i])
            left = next_level_ptr + (child_p_left + children_left - level_ptr) // k
        else:
            left = parent_left
        if right_idx != k-1:
            for i in range(child_p_right, right+1):
                m = max(m, seg[i])
            right = next_level_ptr + (child_p_right - 1 - level_ptr) // k
        else:
            right = parent_right
        level += 1
        level_ptr = level_ptrs[level][0]
        next_level_ptr = level_ptrs[level+1][0]
    for i in range(left, right+1):
        m = max(m, seg[i])
    return m

def print_tree(seg, level_ptrs, data):
    level = len(level_ptrs)-1
    while level >= 0:
        level_ptr, num_elements = level_ptrs[level]
        print(seg[level_ptr:level_ptr+num_elements])
        level -= 1
    print(data)

'''
#Print tree
k = 3
data = rand_list(10, 100)
seg, level_ptrs = gen_tree(data)
print_tree(seg, level_ptrs, data)
'''


'''
# Single query
k=3
data = [39, 79, 14, 19, 1, 13, 16, 97, 97, 62, 29, 21, 60, 23, 29, 59, 7]
#rand_list(17, 100)
seg, level_ptrs = gen_tree(data)
print_tree(seg, level_ptrs, data)
print(seg)
print(level_ptrs)
print(query(1, 4, seg, level_ptrs, data))
print(max(data[1:4+1]))
'''


# Testing
k=16
data = rand_list(1000, 1000000)
seg, level_ptrs = gen_tree(data)

print("Tree overhead: {:.2%}".format(((len(seg) + len(level_ptrs) + len(data)) / len(data) - 1)))
print("Testing all ranges...")

passed = True
for i in range(len(data)):
    for j in range(i, len(data)):
        if max(data[i:j+1]) != query(i, j, seg, level_ptrs, data):
            print("Miss: [{},{}]".format(i, j))
            passed = False
if passed:
    print("Passed all tests")
else:
    print("Failed some tests")
