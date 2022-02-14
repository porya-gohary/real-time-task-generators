#!/usr/bin/env python3
import math
class task:
    def __init__(self, **kwargs):
        """Initialize a task."""
        self.name=kwargs.get('name', '')
        self.phase=kwargs.get('phase', '')
        self.bcet=int(math.ceil(kwargs.get('wcet', 0)*0.7))
        self.wcet=kwargs.get('wcet', 0)
        self.period=kwargs.get('period', 0)
        self.deadline=kwargs.get('deadline', 0)
        self.pe=kwargs.get('pe', 0)
        # Assigned after DAG Genereated
        self.parent = []
        self.child = []
        self.isLeaf = False
        self.level = 0

    def __str__(self):
        res = "%-9s PE=%2s BCET=%-5.1f WCET=%-5.1f Period=%7s Deadline=%7s" \
            % (self.name, self.pe, self.bcet, self.wcet, self.period,self.deadline)
        return res

    def get_data (self):
        return [self.name,self.phase, self.bcet , self.wcet
                , self.period,self.deadline]

    def __repr__(self):
        return repr((self.name, self.phase, self.bcet , self.wcet
                , self.period,self.deadline))