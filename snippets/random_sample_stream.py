
# Generate the stream of data

import random
import time
from tqdm import tqdm  # For progress bar

stream = (random.randint(0, 100) for _ in range(1000))

# Supose we have a reservoir of s=10 elements

s = 100
reservoir = list()

# First, include the ten first elements into the reservoir

for _ in range(s):
    reservoir.append(next(stream))

# Now loop from the stream catching elements with probability s/(n+1).
# This is acomplished because:
#
# Prob of an element been chosen when we have seen n elemens = s/n (starting case of induction)
# Prob that we choose the following element = s/(n+1) (because that's what we want and we can controll that)
#
# The REAL problem is check that if we choose an element with s/(n+1) prob. ALL elements in the set (s) will have
# probabilities of been chosen s/(n+1). Every element in the step n+1 come from the old set (step n) or have been
# choosen in the step (n+1). If the element have been chosen has probability s/(n+1) as seen. If the element was in
# the old set it has probability of been chosen:
#
#     prob_choosen_n+1 = prob_choosen_n * prob_not_been_substituted = s/n * prob_not_been_substituted
#
#   Then prob_not_been_substituted = 1 - prob_been_substituted = 1 - ( prob_selec_to_substitute * prob_need_to_substutite )
#                                  = 1 - ( 1/s * s/(n+1) = n/(n+1)
#
# Recall that prob_need_to_substutite is s/(n+1) because that's the probability that the new element in step n+1
# will be choosen and therefore another will be substituted. So finally:
#
#   prob_choosen_n+1 = s/n * prob_not_been_substituted = s/n * n/(n+1) = s / (n+1)
#

for element in tqdm(stream):

    # Simulate latency
    time.sleep(0.005)

    x = random.randint(0, s)
    if x < s:
        reservoir[x] = element

print(reservoir)
