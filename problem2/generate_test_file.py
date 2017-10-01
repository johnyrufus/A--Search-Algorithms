#!/usr/bin/env python3
# generate_test_file.py : Generate random test file
# Johny

import random
from datetime import datetime

# Number of users.
n = 50
# maximum number for group size
limit = 3


def generate_test_file():

    random.seed(datetime.now())
    users = ['user'+str(i) for i in range(n)]

    lines = []
    for i, user in enumerate(users):
        group_size = random.randint(0, limit)
        # Make sure to limit to group size and not include current user
        likes = random.sample(users[:i]+users[i+1:], random.randint(0, limit-1))
        # Everyone other than the user and the likes list is eligible for the dislike list
        dislikes_eligible = set(users) - set(likes + [user])
        dislikes = random.sample(list(dislikes_eligible), random.randint(0, len(dislikes_eligible)-1))
        likes_str = '_' if len(likes) == 0 else ','.join(likes)
        dislikes_str = '_' if len(dislikes) == 0 else ','.join(dislikes)
        lines.append(' '.join([user, str(group_size), likes_str, dislikes_str]))

    with open('input_large_{}.txt'.format(n), 'w') as f:
        f.write('\n'.join(lines))

generate_test_file()
