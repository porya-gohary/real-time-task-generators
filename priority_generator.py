#!/usr/bin/env python3
"""
priority generator for a specific taskset

Usage:
    priority_generator               [-t FILE] [options]

Options:
    --taskset FILE, -t FILE          taskset csv file [default: taskset-0.csv]
    --method=N, -m N                 priority assigning method (0: Rate-monotonic,1: Deadline-monotonic,2: Earliest deadline first (EDF)) [default: 0]
    --version, -v                    show version and exit
    --help, -h                       show this message
"""

import sys
import os
from math import ceil, floor, gcd
from random import randint
from lxml import etree as ET
import lib.task as task
import lib.job as job
import re
import graphviz
from docopt import docopt
import csv


## calculate least common multiple of two number
def lcm(a, b):
    return abs(a * b) // gcd(a, b) if a and b else 0


## calculate hyperperiod of a taskset
def cal_hyperperiod(task_set):
    h = 1
    for t in task_set:
        h = lcm(h, t.period)
    return h


## generate priority of a taskset (JLFP)
def generate_priority(task_set, hyperperiod, method=0):
    """
    Supported Methods:
    0 -> Rate-monotonic
    1 -> Deadline-monotonic
    2 -> The Earliest deadline first (EDF)
    """
    job_set = []
    for t in task_set:
        for i in range(hyperperiod // t.period):
            job_set.append(
                job.job(name=t.name, jitter=t.jitter, bcet=t.bcet, wcet=t.wcet, period=t.period, deadline=t.deadline,
                        pe=t.pe, instance_num=i))
    if (method == 0):
        sorted_job_set = sorted(job_set, key=lambda job: job.period)
        for priority, j in enumerate(sorted_job_set):
            j.priority = priority
    elif (method == 1):
        sorted_job_set = sorted(job_set, key=lambda job: job.deadline)
        for priority, j in enumerate(sorted_job_set):
            j.priority = priority
    elif (method == 2):
        sorted_job_set = sorted(job_set, key=lambda job: job.absolute_deadline)
        for priority, j in enumerate(sorted_job_set):
            j.priority = priority
    else:
        print("Selected method not valid")
        sys.exit(1)
    sorted_job_set = sorted(sorted_job_set, key=lambda job: job.job_name)
    # for priority, j in enumerate(sorted_job_set):
    #     print(j)
    return sorted_job_set


def read_csv(file):
    taskset = []
    try:
        with open(file, 'r') as read_obj:
            # csv_reader = csv.reader(read_obj)
            csv_dict_reader = csv.DictReader(read_obj)
            # Iterate over each row in the csv using reader object and make tasks
            for row in csv_dict_reader:
                taskset.append(
                    task.task(name=row['Name'], jitter=int(row['Jitter']), bcet=int(row['BCET']), wcet=int(row['WCET']),
                              period=int(row['Period']), deadline=int(row['Deadline']), pe=int(row['PE'])))
        return taskset
    except Exception as e:
        print(e)
        print("ERROR: reading taskset is not possible")
        sys.exit(1)


def write_csv(job_set, taskset_name):
    try:
        header = ['Name', 'Arrival min.', 'Arrival max.', 'BCET', 'WCET', 'Abs. deadline', 'PE', 'Priority']
        with open("jobset-"+taskset_name + '.csv', 'w', encoding='UTF8') as f:
            writer = csv.writer(f)
            writer.writerow(header)
            for j in job_set:
                writer.writerow(j.get_data(True))
                
    except Exception as e:
        print(e)
        print("ERROR: save")
        sys.exit(1)


def main():
    args = docopt(__doc__, version='0.5.0')
    task_set = read_csv(args['--taskset'])
    hyperperiod = cal_hyperperiod(task_set)
    taskset_name = os.path.splitext(os.path.basename(args['--taskset']))[0]
    job_set = generate_priority(task_set, hyperperiod, int(args['--method']))
    write_csv(job_set,taskset_name)

if __name__ == '__main__':
    main()
