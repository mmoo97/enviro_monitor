import datetime
import vars
import os


data_labels = ("date", "time", "temp", "intensity", "red", "green", "blue")


def parse_year(directory):
    pass


def parse_month(directory, year, month):
    pass


def parse_day(directory, year, month, day):
    pass


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


