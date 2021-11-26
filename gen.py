import random
import json

file = open("Users.json", "r")
users = json.load(file)

for u in users:
    u['schedule'] = []
    for d in range(0, u['devices']):
        day_start = random.randint(0, 6)
        day_end = random.randint(day_start, 6)
        hour_start = round(random.uniform(0, 23), 1)
        hour_end = round(random.uniform(hour_start, 23), 1)
        # sched = ((day_start, day_end),(hour_start, hour_end))
        sched = f"{day_start}-{day_end}/{hour_start}-{hour_end}"
        u['schedule'].append(sched)

json_string = json.dumps(users)

file = open("NewUsers.json", "w")
file.write(json_string)
