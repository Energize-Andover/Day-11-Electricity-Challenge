"""
#
# File:              ChallengeProject.py
# Author:            danIv (Daniel Ivanovich)
# Created:           08/06/2018
# Description:       Finds electrical energy used during nights in AHS for the calendar years 2016/17 and 2017/18.
#
"""

import pandas as pd
import os

PART_1_PATH_2016 = os.path.join('CSVs', 'AHS201617Part1.csv')
PART_2_PATH_2016 = os.path.join('CSVs', 'AHS201617Part2.csv')

PART_1_PATH_2017 = os.path.join('CSVs', 'AHS201718Part1.csv')
PART_2_PATH_2017 = os.path.join('CSVs', 'AHS201718Part2.csv')

paths = [PART_1_PATH_2016, PART_2_PATH_2016, PART_1_PATH_2017, PART_2_PATH_2017]
first_last_days = [[[(8, 31), (12, 31)]], [[(1, 1), (6, 16)]], [[(9, 7), (12, 31)]], [[(1, 1), (6, 29)]]]
days_off = [[(9, 5), (10, 3), (10, 10), (10, 11), (10, 12), (11, 8), (11, 11), (11, 24), (11, 25)],
            [(1, 2), (1, 16), (4, 17), (5, 29)],
            [(9, 21), (10, 9), (11, 9), (11, 10), (11, 23), (11, 24)],
            [(1, 1), (1, 15), (5, 28)]]
vacation_day_ranges = [[[(12, 26), (12, 30)]],
                       [[(2, 20), (2, 24)], [(4, 17), (4, 21)]],
                       [[(12, 25), (12, 29)]],
                       [[(2, 19), (2, 23)], [(4, 16), (4, 20)]]]
snow_days = [[], [],
             [(10, 30), (10, 31), (11, 1)],
             [(1, 4), (1, 5), (1, 17), (3, 8), (3, 9), (3, 13), (3, 14)]]
saturdays = [[], [], [],
             [(4, 28), (5, 12)]]


def read_csv(file_path):
    return pd.read_csv(file_path, skipfooter=3, engine='python')


def date_in_list(df, list, index):
    bools = []
    for date in df['Unnamed: 0']:
        bools.append((date.month, date.day) in list[index])

    return pd.Series(bools)


def date_in_list_range(df, list, index):
    bools = []
    for date in df['Unnamed: 0']:
        for range in list[index]:
            bools.append(range[0] <= (date.month, date.day) <= range[1])

    return pd.Series(bools)


df_sum = 0
filtered_sum = 0
for index, path in enumerate(paths):
    df = read_csv(path)
    df['Unnamed: 0'] = pd.to_datetime(df['Unnamed: 0'], format='%Y-%m-%d %H:%M:%S', utc=False)

    saturday = date_in_list(df, saturdays, index)

    # When school is not in session:
    weekend = df['Unnamed: 0'].dt.weekday >= 5 & ~saturday
    vacation = date_in_list_range(df, vacation_day_ranges, index)
    day_off = date_in_list(df, days_off, index)
    snow_day = date_in_list(df, snow_days, index)

    weekday = df['Unnamed: 0'].dt.weekday < 5 | saturday
    after_10 = df['Unnamed: 0'].dt.hour >= 22
    before_4 = df['Unnamed: 0'].dt.hour < 4

    bools = []
    for date in df['Unnamed: 0']:
        bools.append(date.hour == 4 and date.minute == 0)

    is_4_sharp = pd.Series(bools)

    school_night = weekday & (after_10 | before_4 | is_4_sharp)

    between_first_last_day = date_in_list_range(df, first_last_days, index)

    df_sum += round(df.sum().sum(), 2)
    df = df[between_first_last_day & (weekend | vacation | day_off | snow_day | school_night)]
    filtered_sum += round(df.sum().sum(), 2)

other_part = df_sum - filtered_sum

print(str(round(other_part / filtered_sum, 3)) + '%')