#!/usr/bin/env python3
"""
A script to convert SAG job set format to segment set.

Usage:
    job_set_to_segment_set                [options]

Options:
    --job-set FILE, -j FILE             job set csv file [default: example.csv]
    --version, -v                       show version and exit
    --help, -h                          show this message
"""

from docopt import docopt
import sys
from pathlib import Path
import csv


class job:
    def __init__(self, **kwargs):
        """Initialize a job."""
        self.task_id = kwargs.get('task_id', '')
        self.job_id = kwargs.get('job_id', '')
        self.arrival_min = kwargs.get('arrival_min', '')
        self.arrival_max = kwargs.get('arrival_max', '')
        self.cost_min = kwargs.get('cost_min', 0)
        self.cost_max = kwargs.get('cost_max', 0)
        self.deadline = kwargs.get('deadline', 0)
        self.priority = kwargs.get('priority', 0)


def read_job_set(file):
    job_set = []
    try:
        with open(file, 'r') as read_obj:
            csv_dict_reader = csv.DictReader(read_obj, skipinitialspace=True)
            # Iterate over each row in the csv using reader object and make jobs
            for row in csv_dict_reader:
                job_set.append(
                    job(task_id=int(row['Task ID']), job_id=int(row['Job ID']), arrival_min=int(row['Arrival min']),
                        arrival_max=int(row['Arrival max']), cost_min=int(row['Cost min']),
                        cost_max=int(row['Cost max']), deadline=int(row['Deadline']), priority=int(row['Priority'])))
        return job_set
    except Exception as e:
        print(e)
        print("ERROR: reading job set is not possible")
        sys.exit(1)


def write_segment_set(file, job_set):
    segments = 'task graphs:\n'
    printed = [False for i in range(len(job_set))]
    job_set.sort(key=lambda x: x.task_id)

    for i in range(0, len(job_set)):
        if not printed[i]:
            segments += "  - id: " + str(job_set[i].task_id) + "\n"
            segments += "    segments:\n"
            for j in range(i, len(job_set)):
                if job_set[i].task_id == job_set[j].task_id:
                    segments += "      - id: " + str(job_set[j].job_id) + "\n"
                    segments += "        arrival min: " + str(job_set[j].arrival_min) + "\n"
                    segments += "        arrival max: " + str(job_set[j].arrival_max) + "\n"
                    segments += "        cost min: " + str(job_set[j].cost_min) + "\n"
                    segments += "        cost max: " + str(job_set[j].cost_max) + "\n"
                    segments += "        deadline: " + str(job_set[j].deadline) + "\n"
                    segments += "        priority: " + str(job_set[j].priority) + "\n"
                    printed[j] = True
    with open(file.with_suffix('.yaml'), 'w') as f:
        f.write(segments)


def main():
    args = docopt(__doc__, version='0.1')
    job_set_file = Path(args['--job-set'])
    job_set = read_job_set(job_set_file)
    write_segment_set(job_set_file, job_set)


if __name__ == '__main__':
    main()
