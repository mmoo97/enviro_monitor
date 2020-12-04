import datetime
import vars
import os


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
    return data_output["temps"]

print(parse_day(vars.data_dir, "2020-05-10"))

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


def write_to_db(db_location):
    import sqlite3

    conn = sqlite3.connect(db_location)

    pass

write_to_db(vars.db_dir)
