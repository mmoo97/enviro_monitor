import datetime
import vars
import os
import sqlite3

data_labels = ("date", "time", "temp", "intensity", "red", "green", "blue")


def parse_year(directory):
    pass


def parse_month(directory, year, month):
    pass


def parse_day(directory, date):
    """
    :param directory: string directory where data files lies
    :param date: string of format 'YYYY-MM-DD'
    :return: requested data as json
    """

    suffix = ".txt"
    data_output = {"date": date, "times": [], "temps": [],
                   "intensity": [], "red": [], "green": [], "blue": []}
    with open((directory + date + suffix), "r") as f:
        for line in f.readlines():
            line = line.split("\t")
            if line[0] != "Date":
                data_output['times'].append(line[1])
                data_output['temps'].append(line[2])
                data_output['intensity'].append(line[3])
                data_output['red'].append(line[4])
                data_output['green'].append(line[5])
                data_output['blue'].append(line[6])
        f.close()
    return data_output


def parse_recent(directory):
    suffix = ".txt"
    now = datetime.datetime.now()
    date = now.strftime("%Y-%m-%d")
    data_output = {}
    with open((directory + date + suffix), "rb") as f:
        f.seek(-2, os.SEEK_END)
        # f.seek(-2, )
        while f.read(1) != b'\n':
            f.seek(-2, os.SEEK_CUR)
        last_line = f.readline().decode().replace('\n', '')
        last_line = last_line.split("\t")
        for i in last_line:
            data_output[data_labels[last_line.index(i)]] = i
        f.close()
        return data_output


def write_to_db(db_location, table, values, raw):

    conn = sqlite3.connect(db_location)
    cur = conn.cursor()

    cur.execute("PRAGMA table_info('{}');".format(table))

    columns = cur.fetchall()
    holders = ""
    col_names = ""
    for name in columns:
        holders = holders + "?"
        col_names = col_names + name[1]

        if name[1] != columns[-1][-5]:
            holders = holders + ","
            col_names = col_names + ", "

    # print(col_names)
    # print(holders)

    command = "INSERT INTO '{}' ({}) VALUES({});".format(table, col_names, holders)
    # command = command.format(values)
    # print(values)
    # 
    # print(command)

    if raw is None:
        cur.execute(command, values)
    else:
        cur.execute(raw, values)

    conn.commit()
    cur.close()


data = parse_day(vars.data_dir, "2020-05-10")
for i in range(len(data['times'])):
    write_to_db(vars.db_dir, str(data['date']), (data['times'][i], data['temps'][i],
                                             data['intensity'][i], data['red'][i],
                                             data['green'][i], data['blue'][i]), None)
