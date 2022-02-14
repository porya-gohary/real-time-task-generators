#!/usr/bin/env python3
"""Task set generation with WATERS benchmark.
From the paper: 'Real world automotive benchmark for free' (WATERS 2015).
some part adapted from https://github.com/tu-dortmund-ls12-rt/end-to-end
"""
from scipy import stats
from scipy.stats import exponweib
from lib.task import task
import numpy as np
import random


def StaffordRandFixedSum(n, u, nsets):
    # deal with n=1 case
    if n == 1:
        return np.tile(np.array([u]), [nsets, 1])

    k = np.floor(u)
    s = u
    step = 1 if k < (k - n + 1) else -1
    s1 = s - np.arange(k, (k - n + 1) + step, step)
    step = 1 if (k + n) < (k - n + 1) else -1
    s2 = np.arange((k + n), (k + 1) + step, step) - s

    tiny = np.finfo(float).tiny
    huge = np.finfo(float).max

    w = np.zeros((n, n + 1))
    w[0, 1] = huge
    t = np.zeros((n - 1, n))

    for i in np.arange(2, (n + 1)):
        tmp1 = w[i - 2, np.arange(1, (i + 1))] * s1[np.arange(0, i)] / float(i)
        tmp2 = w[i - 2, np.arange(0, i)] * s2[np.arange((n - i), n)] / float(i)
        w[i - 1, np.arange(1, (i + 1))] = tmp1 + tmp2;
        tmp3 = w[i - 1, np.arange(1, (i + 1))] + tiny;
        tmp4 = np.array((s2[np.arange((n - i), n)] > s1[np.arange(0, i)]))
        t[i - 2, np.arange(0, i)] = (tmp2 / tmp3) * tmp4 + (1 - tmp1 / tmp3) * (np.logical_not(tmp4))

    m = nsets
    x = np.zeros((n, m))
    rt = np.random.uniform(size=(n - 1, m))  # rand simplex type
    rs = np.random.uniform(size=(n - 1, m))  # rand position in simplex
    s = np.repeat(s, m);
    j = np.repeat(int(k + 1), m);
    sm = np.repeat(0, m);
    pr = np.repeat(1, m);

    for i in np.arange(n - 1, 0, -1):  # iterate through dimensions
        e = (rt[(n - i) - 1, ...] <= t[i - 1, j - 1])  # decide which direction to move in this dimension (1 or 0)
        sx = rs[(n - i) - 1, ...] ** (1 / float(i))  # next simplex coord
        sm = sm + (1 - sx) * pr * s / float(i + 1)
        pr = sx * pr
        x[(n - i) - 1, ...] = sm + pr * e
        s = s - e
        j = j - e  # change transition table column if required

    x[n - 1, ...] = sm + pr * s

    # iterated in fixed dimension order but needs to be randomised
    # permute x row order within each column
    for i in range(0, m):
        x[..., i] = x[np.random.permutation(n), i]

    return np.transpose(x);


def gen_tasksets(
        number_of_sets=100, number_of_task=15, util_req=0.5,
        period_pdf=[0.03, 0.02, 0.02, 0.25, 0.40, 0.03, 0.2, 0.01, 0.04],
        scalingFlag=True, threshold=0.1, cylinder=4, sumRunnable=True):
    """Main function to generate task sets with the WATERS benchmark.
    Variables:
    number_of_sets: number of task sets
    util_req: required utilization
    period_pdf: statistical distribution
    scalingFlag: make WCET out of ACET with scaling
    threshold: accuracy of the required utilization
    cylinder: specific value for WATERS
    """
    sets = []
    for j in range(number_of_sets):
        taskset = []
        # Create runnable periods.
        dist = stats.rv_discrete(name='periods',
                                 values=([1, 2, 5, 10, 20, 50, 100, 200, 1000],
                                         period_pdf))
        runnables = (number_of_task * number_of_sets)  # number of runnables

        sys_task_periods = dist.rvs(size=runnables)
        # print (sys_task_periods)

        # Build tasks from runnables.
        utilizations = StaffordRandFixedSum(number_of_task, util_req, number_of_sets).flatten()
        # print (utilizations)
        for i in range(len(sys_task_periods)):
            wcet = utilizations[i] * sys_task_periods[i]
            taskset.append(task(wcet=wcet,period=sys_task_periods[i],deadline=sys_task_periods[i]))
            # temp = np.c_[utilizations[i], wcet / sys_task_periods[i], sys_task_periods[i],  wcet]
            # print (wcet)
        # for t in range(np.size(temp,0)):
        #     taskset.append(task(wcet=temp[t][3],period=temp[t][2],deadline=temp[t][2]))
        # Shuffke the task set.
        random.shuffle(taskset)
        sets.append(taskset)
    return sets
