import os

directory = '/etc/room_temp/room_data'

filenames = []

for filename in os.listdir(directory):
    filenames.append(filename)

filenames = sorted(filenames)

with open("dump.txt", "a") as main_file:
    for name in filenames:
        with open(directory + "/" + name, "r") as sub_file:
            content = sub_file.readlines()
            main_file.writelines(content)

with open("dump.txt", "r+") as f:
    d = f.readlines()
    f.seek(0)
    count = 0
    f.write(d[0])
    for i in d:
        if i[0] != "D":
            f.write(i)
            count += 1
    f.truncate()
    print(count)