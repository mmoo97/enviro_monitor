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
    data_output = {"date": date, "time": list(), "temp": list(),
                   "intensity": list(), "red": list(), "green": list(), "blue": list()}
    with open((directory + date + suffix), "r") as f:
        f.readline()
        count = 0
        for line in f.readlines():
            print(line)
            last_line = f.readline().replace('\n', '')
            last_line = last_line.split("\t")
        # todo: pick up from this point
            data_output["time"].append(last_line[1])
            count = count + 1
            if count == 20:
                break
        f.close()
    pass

parse_day(vars.data_dir, "2020-04-01")

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


