#!/usr/bin/env python3
import math
from lib.task import task


class job(task):
    def __init__(self, **kwargs):
        """Initialize a job."""
        super().__init__(**kwargs)
        self.instance_num = kwargs.get('instance_num', '')
        self.priority = kwargs.get('priority', '')
        self.earliest_arrival = self.period * self.instance_num
        self.latest_arrival = (self.period * self.instance_num) + self.jitter
        self.absolute_deadline = self.earliest_arrival + self.deadline
        self.job_name = self.name + ',' + str(self.instance_num)

    def __str__(self):
        res = "%-7s\tPE=%2s\tBCET=%-5.1f\tWCET=%-5.1f\tArrival window=[%7s, %7s]\tAbs. deadline=%7s\tPriority=%4s" \
              % (self.job_name, self.pe, self.bcet, self.wcet, self.earliest_arrival, self.latest_arrival,
                 self.absolute_deadline, self.priority)
        return res

    def __repr__(self):
        return repr((self.job_name, self.pe, self.jitter, self.bcet, self.wcet
                     , self.period, self.absolute_deadline))

    def get_data(self, mapping=False, sag_format=False):
        if not mapping and not sag_format:
            return [self.job_name, self.earliest_arrival, self.latest_arrival, self.bcet, self.wcet
                , self.absolute_deadline, self.priority]

        elif sag_format:
            return [self.get_id(), self.instance_num, self.earliest_arrival, self.latest_arrival, self.bcet, self.wcet
                , self.absolute_deadline, self.priority]
        else:
            return [self.job_name, self.earliest_arrival, self.latest_arrival, self.bcet, self.wcet
                , self.absolute_deadline, self.pe, self.priority]
