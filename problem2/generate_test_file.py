import random
import sys
from datetime import datetime

n = 50
def generate_test_file():

    random.seed(datetime.now())
    users = ['user'+str(i) for i in range(n)]

    lines = []
    for i,user in enumerate(users):
        group_size = random.randint(0, n-1)
        likes = random.sample(users[:i]+users[i+1:], random.randint(0, n-2))
        dislikes_eligible = set(users) - set(likes + [user])
        dislikes = random.sample(list(dislikes_eligible), random.randint(0, len(dislikes_eligible)-1))
        likes_str = '_' if len(likes) == 0 else ','.join(likes)
        dislikes_str = '_' if len(dislikes) == 0 else ','.join(dislikes)
        lines.append(' '.join([user, str(group_size), likes_str, dislikes_str]))

    with open('input_large_{}.txt'.format(n), 'w') as f:
        f.write('\n'.join(lines))

generate_test_file()
