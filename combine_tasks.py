#!/usr/bin/env python3
"""
A script to combine tasks with the same period to one task.

Usage:
    combine_tasks                [options]

Options:
    --task-set FILE, -t FILE            task set csv file [default: example.csv]
    --version, -v                       show version and exit
    --help, -h                          show this message
"""

from docopt import docopt
import sys
import os
from pathlib import Path
import csv
import lib.task as task

debug_flag = False  # flag to have breakpoint() when errors occur


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


def write_csv(job_set, taskset_name, sag_format=False):
    try:
        if not sag_format:
            header = ['Name', 'Arrival min.', 'Arrival max.', 'BCET', 'WCET', 'Abs. deadline', 'PE', 'Priority']
            with open("jobset-" + taskset_name + '.csv', 'w', encoding='UTF8') as f:
                writer = csv.writer(f)
                writer.writerow(header)
                for j in job_set:
                    writer.writerow(j.get_data(mapping=True))
        else:
            header = ['Task ID', 'Job ID', 'Arrival min', 'Arrival max', 'Cost min', 'Cost max', 'Deadline', 'Priority']
            with open("jobset-" + taskset_name + '.csv', 'w', encoding='UTF8') as f:
                writer = csv.writer(f)
                writer.writerow(header)
                for j in job_set:
                    writer.writerow(j.get_data(mapping=False, sag_format=True))
    except Exception as e:
        print(e)
        print("ERROR: save")
        sys.exit(1)


def combine_tasks(task_set):
    new_task_set = []
    for t in task_set:
        if not new_task_set:
            new_task_set.append(t)
        else:
            for nt in new_task_set:
                if t.period == nt.period:
                    nt.wcet += t.wcet
                    nt.bcet += t.bcet
                    break
            else:
                new_task_set.append(t)
    return new_task_set

def combine_tasks_with_lowest_period(task_set):
    new_task_set = []
    # sort task set by period
    task_set.sort(key=lambda x: x.period)
    # determine the lowest period
    lowest_period = task_set[0].period
    # combine tasks with the same period
    for t in task_set:
        if not new_task_set:
            new_task_set.append(t)
        elif t.period == lowest_period:
            for nt in new_task_set:
                if t.period == nt.period:
                    nt.wcet += t.wcet
                    nt.bcet += t.bcet
                    break
        else:
            new_task_set.append(t)
    return new_task_set

def write_taskset(task_set, taskset_name):
    ###
    # Save data.
    ###
    print("= Save data =")

    try:

        header = ['Name', 'Jitter', 'BCET', 'WCET', 'Period', 'Deadline', 'PE']

        with open(taskset_name + '.csv', 'w', encoding='UTF8') as f:
            writer = csv.writer(f)

            # write the header
            writer.writerow(header)

            for t in task_set:
                writer.writerow(t.get_data(True))

    except Exception as e:
        print(e)
        print("ERROR: save")
        if debug_flag:
            breakpoint()
        else:
            return


def main():
    args = docopt(__doc__, version='0.5.0')
    print(args)
    task_set = read_csv(args['--task-set'])
    taskset_name = os.path.splitext(os.path.basename(args['--task-set']))[0]+"-combined"
    new_task_set = combine_tasks_with_lowest_period(task_set)
    write_taskset(new_task_set, taskset_name)


if __name__ == '__main__':
    main()
