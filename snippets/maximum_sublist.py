# Only the sum
def mssl(l):
    best = cur = 0
    for i in l:
        cur = max(cur + i, 0)
        best = max(best, cur)
    return best


def mssl(iterable):
    best_sum = 0
    current_sum = 0
    best_final_index = 0
    best_initial_index = 0
    current_initial_index = 0

    for i, value in enumerate( iterable ):

        if current_sum + value > 0:
            current_sum += value
        else:
            # We have found a breaking point in our array. Adding values before this point
            # to subarrays formed after this point is useless because the sum will be lower.
            current_initial_index = i + 1
            current_sum = 0

        if current_sum > best_sum:
            best_sum = current_sum
            best_initial_index = current_initial_index
            best_final_index = i+1

    return iterable[best_initial_index:best_final_index], best_sum

print(mssl([4, -2, -8, 5, -2, 7, 7, 2, -6, 5]))