#!/usr/bin/env python3
"""Task set generation with WATERS benchmark.
From the paper: 'Real world automotive benchmark for free' (WATERS 2015).
This part adapted from https://github.com/tu-dortmund-ls12-rt/end-to-end
"""
from scipy import stats
from scipy.stats import exponweib
from lib.task import task
import numpy as np
import random


###
# Task set generation.
###
def sample_runnable_acet(period, amount=1, scalingFlag=False):
    """Create runnables according to the WATERS benchmark.
    scalingFlag: make WCET out of ACET with scaling
    """
    # Parameters from WATERS 'Real World Automotive Benchmarks For Free'
    if period == 1:
        # Pull scaling factor.
        scaling = np.random.uniform(1.3, 29.11, amount)  # between fmin fmax
        # Pull samples with weibull distribution.
        dist = exponweib(1, 1.044, loc=0, scale=1.0/0.214)
        samples = dist.rvs(size=amount)
        while True:
            outliers_detected = False
            for i in range(len(samples)):
                # Check if they are in the range.
                if samples[i] < 0.34 or samples[i] > 30.11:
                    outliers_detected = True
                    samples[i] = dist.rvs(size=1)
            # Case: Some samples had to be pulled again.
            if outliers_detected:
                continue
            # Case: All samples are in the range.
            if scalingFlag:  # scaling
                return list(0.001 * samples*scaling)
            else:
                return list(0.001 * samples)

    # In the following same structure but different values.

    if period == 2:
        scaling = np.random.uniform(1.54, 19.04, amount)
        dist = exponweib(1, 1.0607440083, loc=0, scale=1.0/0.2479463059)
        samples = dist.rvs(size=amount)
        while True:
            outliers_detected = False
            for i in range(len(samples)):
                if samples[i] < 0.32 or samples[i] > 40.69:
                    outliers_detected = True
                    samples[i] = dist.rvs(size=1)
            if outliers_detected:
                continue
            if scalingFlag:
                return list(0.001 * samples*scaling)
            else:
                return list(0.001 * samples)

    if period == 5:
        scaling = np.random.uniform(1.13, 18.44, amount)
        dist = exponweib(1, 1.00818633, loc=0, scale=1.0/0.09)
        samples = dist.rvs(size=amount)
        while True:
            outliers_detected = False
            for i in range(len(samples)):
                if samples[i] < 0.36 or samples[i] > 83.38:
                    outliers_detected = True
                    samples[i] = dist.rvs(size=1)
            if outliers_detected:
                continue
            if scalingFlag:
                return list(0.001 * samples*scaling)
            else:
                return list(0.001 * samples)

    if period == 10:
        scaling = np.random.uniform(1.06, 30.03, amount)
        dist = exponweib(1, 1.0098, loc=0, scale=1.0/0.0985)
        samples = dist.rvs(size=amount)
        while True:
            outliers_detected = False
            for i in range(len(samples)):
                if samples[i] < 0.21 or samples[i] > 309.87:
                    outliers_detected = True
                    samples[i] = dist.rvs(size=1)
            if outliers_detected:
                continue
            if scalingFlag:
                return list(0.001 * samples*scaling)
            else:
                return list(0.001 * samples)

    if period == 20:
        scaling = np.random.uniform(1.06, 15.61, amount)
        dist = exponweib(1, 1.01309699673984310, loc=0, scale=1.0/0.1138186679)
        samples = dist.rvs(size=amount)
        while True:
            outliers_detected = False
            for i in range(len(samples)):
                if samples[i] < 0.25 or samples[i] > 291.42:
                    outliers_detected = True
                    samples[i] = dist.rvs(size=1)
            if outliers_detected:
                continue
            if scalingFlag:
                return list(0.001 * samples*scaling)
            else:
                return list(0.001 * samples)

    if period == 50:
        scaling = np.random.uniform(1.13, 7.76, amount)
        dist = exponweib(1, 1.00324219159296302, loc=0,
                         scale=1.0/0.05685450460)
        samples = dist.rvs(size=amount)
        while True:
            outliers_detected = False
            for i in range(len(samples)):
                if samples[i] < 0.29 or samples[i] > 92.98:
                    outliers_detected = True
                    samples[i] = dist.rvs(size=1)
            if outliers_detected:
                continue
            if scalingFlag:
                return list(0.001 * samples*scaling)
            else:
                return list(0.001 * samples)

    if period == 100:
        scaling = np.random.uniform(1.02, 8.88, amount)
        dist = exponweib(1, 1.00900736028318527, loc=0,
                         scale=1.0/0.09448019812)
        samples = dist.rvs(size=amount)
        while True:
            outliers_detected = False
            for i in range(len(samples)):
                if samples[i] < 0.21 or samples[i] > 420.43:
                    outliers_detected = True
                    samples[i] = dist.rvs(size=1)
            if outliers_detected:
                continue
            if scalingFlag:
                return list(0.001 * samples*scaling)
            else:
                return list(0.001 * samples)

    if period == 200:
        scaling = np.random.uniform(1.03, 4.9, amount)
        dist = exponweib(1, 1.15710612360723798, loc=0,
                         scale=1.0/0.3706045664)
        samples = dist.rvs(size=amount)
        while True:
            outliers_detected = False
            for i in range(len(samples)):
                if samples[i] < 0.22 or samples[i] > 21.95:
                    outliers_detected = True
                    samples[i] = dist.rvs(size=1)
            if outliers_detected:
                continue
            if scalingFlag:
                return list(0.001 * samples*scaling)
            else:
                return list(0.001 * samples)

    if period == 1000:
        # No weibull since the range from 0.37 to 0.46 is too short to be
        # modeled by weibull properly.
        scaling = np.random.uniform(1.84, 4.75, amount)
        if scalingFlag:
            return list(0.001 * np.random.uniform(0.37, 0.46, amount)*scaling)
        else:
            return list(0.001 * np.random.uniform(0.37, 0.46, amount))


def sum_same_period_tasks(taskset,number_of_task=15, period=[1, 2, 5, 10, 20, 50, 100, 200, 1000]):
    newtaskset = []
    # for t in taskset:
    #     print (t)
    sorted_task_set = sorted(taskset, key=lambda task: task.period)
    n_tasks=len(taskset)
    if(n_tasks <= number_of_task):
        return taskset
    flag = False
    index =0
    for p in period:
        sumwcet=0
        if (flag):
            break
        for i in range(len(taskset)):
            if(p==taskset[i].period):
                if(sumwcet+ taskset[i].wcet <= p):
                    sumwcet+= taskset[i].wcet
                    n_tasks-=1
                else:
                    newtaskset.append(task(wcet=sumwcet, period=p, deadline=p))
                    sumwcet=0
                if(number_of_task == n_tasks):
                    newtaskset.append(task(wcet=sumwcet, period=p, deadline=p))
                    index = i+1
                    break
                    flag =True
        if(not flag):
            newtaskset.append(task(wcet=sumwcet, period=p, deadline=p))
        else:
            for i in range(index,len(taskset)):
                newtaskset.append(taskset[i])
    # print("-------- After")
    # for t in newtaskset:
    #     print (t)
    # print(len(newtaskset))
    return newtaskset


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

    while True:
        taskset = []
        # Create runnable periods.
        dist = stats.rv_discrete(name='periods',
                                 values=([1, 2, 5, 10, 20, 50, 100, 200, 1000],
                                         period_pdf))
        runnables = (30000*number_of_sets)  # number of runnables

        sys_runnable_periods = dist.rvs(size=runnables)

        # Count runnables.
        sys_runnables_period_0001_amount = 0
        sys_runnables_period_0002_amount = 0
        sys_runnables_period_0005_amount = 0
        sys_runnables_period_0010_amount = 0
        sys_runnables_period_0020_amount = 0
        sys_runnables_period_0050_amount = 0
        sys_runnables_period_0100_amount = 0
        sys_runnables_period_0200_amount = 0
        sys_runnables_period_1000_amount = 0

        for period in sys_runnable_periods:
            if period == 1:
                sys_runnables_period_0001_amount += 1
            elif period == 2:
                sys_runnables_period_0002_amount += 1
            elif period == 5:
                sys_runnables_period_0005_amount += 1
            elif period == 10:
                sys_runnables_period_0010_amount += 1
            elif period == 20:
                sys_runnables_period_0020_amount += 1
            elif period == 50:
                sys_runnables_period_0050_amount += 1
            elif period == 100:
                sys_runnables_period_0100_amount += 1
            elif period == 200:
                sys_runnables_period_0200_amount += 1
            elif period == 1000:
                sys_runnables_period_1000_amount += 1
            else:
                print("ERROR")

        # Build tasks from runnables.

        # (PERIOD = 1)
        # Random WCETs.
        wcets = sample_runnable_acet(1, sys_runnables_period_0001_amount,
                                     scalingFlag)
        # Use WCETs to create tasks.
        for i in range(sys_runnables_period_0001_amount):
            taskset.append(task(wcet=wcets[i], period=1, deadline=1))

        # (PERIOD = 2)
        wcets = sample_runnable_acet(2, sys_runnables_period_0002_amount,
                                     scalingFlag)
        for i in range(sys_runnables_period_0002_amount):
            taskset.append(task(wcet=wcets[i], period=2, deadline=2))

        # (PERIOD = 5)
        wcets = sample_runnable_acet(5, sys_runnables_period_0005_amount,
                                     scalingFlag)
        for i in range(sys_runnables_period_0005_amount):
            taskset.append(task(wcet=wcets[i], period=5, deadline=5))

        # (PERIOD = 10)
        wcets = sample_runnable_acet(10, sys_runnables_period_0010_amount,
                                     scalingFlag)
        for i in range(sys_runnables_period_0010_amount):
            taskset.append(task(wcet=wcets[i], period=10, deadline=10))

        # (PERIOD = 20)
        wcets = sample_runnable_acet(20, sys_runnables_period_0020_amount,
                                     scalingFlag)
        for i in range(sys_runnables_period_0020_amount):
            taskset.append(task(wcet=wcets[i], period=20, deadline=20))

        # (PERIOD = 50)
        wcets = sample_runnable_acet(50, sys_runnables_period_0050_amount,
                                     scalingFlag)
        for i in range(sys_runnables_period_0050_amount):
            taskset.append(task(wcet=wcets[i], period=50, deadline=50))

        # (PERIOD = 100)
        wcets = sample_runnable_acet(100, sys_runnables_period_0100_amount,
                                     scalingFlag)
        for i in range(sys_runnables_period_0100_amount):
            taskset.append(task(wcet=wcets[i], period=100, deadline=100))

        # (PERIOD = 200)
        wcets = sample_runnable_acet(200, sys_runnables_period_0200_amount,
                                     scalingFlag)
        for i in range(sys_runnables_period_0200_amount):
            taskset.append(task(wcet=wcets[i], period=200, deadline=200))

        # (PERIOD = 1000)
        wcets = sample_runnable_acet(1000, sys_runnables_period_1000_amount,
                                     scalingFlag)
        for i in range(sys_runnables_period_1000_amount):
            taskset.append(task(wcet=wcets[i], period=1000, deadline=1000))


        # Shuffke the task set.
        random.shuffle(taskset)
        sets = []

        # Select subset of tasks using the subset-sum approximation algorithm.

        for j in range(number_of_sets):
            thisset = taskset[:3000]
            taskset = taskset[3000:]
            util = 0.0
            i = 0
            for tasks in thisset:
                util += tasks.wcet/tasks.period
                i = i + 1
                if util > util_req:
                    break

            if(util <= util_req + threshold):
                thisset = thisset[:i]
            else:
                i = i - 1
                initialSet = thisset[:i]
                remainingTasks = thisset[i:]
                tasks = remainingTasks[0]
                util -= tasks.wcet/tasks.period

                while (util < util_req):
                    tasks = remainingTasks[0]
                    if (util + tasks.wcet/tasks.period
                            <= util_req + threshold):
                        util += tasks.wcet/tasks.period
                        initialSet.append(tasks)
                    remainingTasks = remainingTasks[1:]
                thisset = initialSet
            if (sumRunnable):
                thisset=sum_same_period_tasks(thisset,number_of_task)
            sets.append(thisset)

        # # Remove task sets that contain just one task.
        # for task_set in sets:
        #     if len(task_set) < 2:
        #         sets.remove(task_set)
        return sets

