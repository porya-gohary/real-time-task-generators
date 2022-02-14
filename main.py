#!/usr/bin/env python3
"""
Taskset Generator

Usage:
    main                [options]

Options:
    --round, -r                         round the numbers [default: False]
    --utilization=N, -u N               system utilization in percent  [default: 50]
    --generator=N, -g N                 task generation algorithm (0: WATERS 1: UUniFast 2: Emberson 3:WATERS (fixed-sum))  [default: 1]
    --ntask=N, -n N                     number of tasks in one taskset  [default: 15]
    --nset=N, -s N                      number of tasksets to generate  [default: 1]
    --npe=N, -m N                       number of processing elements  [default: 4]
    --version, -v                       show version and exit
    --help, -h                          show this message
"""

import lib.generator_WATERS as waters
import lib.generator_UUNIFAST as uunifast
import lib.generator_Emberson as emberson
import lib.generator_WATERS_fixedsum as waters_fs
import lib.task as task
import lib.transformer as trans

from docopt import docopt
import csv

debug_flag = False  # flag to have breakpoint() when errors occur


def generate_taskset(args):
    ###
    # Task set generation.
    ###
    print(">>> Task set generate <<<")
    # Required utilization:
    req_uti = float(args['--utilization']) / 100.0
    n_task = int(args['--ntask'])
    round_c = args['--round']
    n_PE = int(args['--npe'])

    # try:
    if int(args['--generator']) == 0:
        # WATERS benchmark
        print("WATERS benchmark.")

        # Statistical distribution for task set generation from table 3
        # of WATERS free benchmark paper.
        profile = [0.03 / 0.85, 0.02 / 0.85, 0.02 / 0.85, 0.25 / 0.85,
                   0.25 / 0.85, 0.03 / 0.85, 0.2 / 0.85, 0.01 / 0.85,
                   0.04 / 0.85]

        # Maximal difference between required utilization and actual
        # utilization is set to 1 percent:
        threshold = 10.0

        # Create task sets from the generator.
        # Each task is a dictionary.
        print("\tCreate task sets.")
        task_sets_waters = []
        while len(task_sets_waters) < 1:
            task_sets_gen = waters_fs.gen_tasksets(
                1, n_task, req_uti, profile, True, threshold / 100.0, 4, True)
            task_sets_waters.append(task_sets_gen[0])
            # Transform tasks to fit framework structure.
            # Each task is an object of utilities.task.Task.
        trans1 = trans.Transformer(task_sets_waters, 100)
        task_sets = trans1.transform_tasks(False, n_PE=n_PE, mapping=0)
        # for t in task_sets[0]:
        #     print(t)
        return task_sets

    elif int(args['--generator']) == 1:
        # UUniFast benchmark.
        print("UUniFast task set generator.")

        # Create task sets from the generator.
        print("\tCreate task sets.")

        # The following can be used for task generation with the
        # UUniFast benchmark without predefined periods.

        # # Generate log-uniformly distributed task sets:
        task_sets_uunifast = uunifast.gen_tasksets(
            n_task, 1, 1, 100, req_uti, rounded=round_c)

        # Generate log-uniformly distributed task sets with predefined
        # periods:
        # periods = [1, 2, 5, 10, 20, 50, 100, 200, 500, 1000]
        # periods = [5, 10, 20, 50, 100, 200, 500, 1000]
        # Interval from where the generator pulls log-uniformly.
        # min_pull = 5
        # max_pull = 2000

        # task_sets_uunifast = uunifast.gen_tasksets_pred(
        #     n_task, 1, min_pull, max_pull, req_uti, periods)

        trans2 = trans.Transformer(task_sets_uunifast, 100)
        task_sets = trans2.transform_tasks(False, n_PE=n_PE, mapping=1)
        return task_sets

    elif int(args['--generator']) == 2:
        # UUniFast benchmark.
        print("Emberson task set generator.")

        # Create task sets from the generator.
        print("\tCreate task sets.")

        task_set_emberson = emberson.gen_tasksets(n=n_task, u=req_uti, nsets=1, permin=10, permax=100, gran=5,
                                                  round_C=round_c, dist="logunif")
        # print (task_set_emberson)
        trans3 = trans.Transformer(task_set_emberson, 1)
        task_sets = trans3.transform_tasks(phase=False, n_PE=n_PE, mapping=2)
        # print (task_sets)
        return task_sets
    elif int(args['--generator']) == 3:
        # WATERS benchmark with fixed-sum utilization
        print("WATERS (fixed-sum) benchmark.")

        # Statistical distribution for task set generation from table 3
        # of WATERS free benchmark paper.
        profile = [0.03 / 0.85, 0.02 / 0.85, 0.02 / 0.85, 0.25 / 0.85,
                   0.25 / 0.85, 0.03 / 0.85, 0.2 / 0.85, 0.01 / 0.85,
                   0.04 / 0.85]

        # Maximal difference between required utilization and actual
        # utilization is set to 1 percent:
        threshold = 10.0

        # Create task sets from the generator.
        # Each task is a dictionary.
        print("\tCreate task sets.")
        task_sets_waters = []
        while len(task_sets_waters) < 1:
            task_sets_gen = waters_fs.gen_tasksets(
                1, n_task, req_uti, profile, True, threshold / 100.0, 4, True)
            task_sets_waters.append(task_sets_gen[0])
            # for t in task_sets_gen:
            #     print(t)
        # Transform tasks to fit framework structure.
        # Each task is an object of utilities.task.Task.
        trans4 = trans.Transformer(task_sets_waters, 100)
        task_sets = trans4.transform_tasks(phase=False, n_PE=n_PE, mapping=1)
        return task_sets

    elif int(args['--generator']) == 4:
        # WATERS benchmark with fixed-sum utilization
        print("WATERS (fixed-sum) benchmark with partitioned task generation.")

        # Statistical distribution for task set generation from table 3
        # of WATERS free benchmark paper.
        profile = [0.03 / 0.85, 0.02 / 0.85, 0.02 / 0.85, 0.25 / 0.85,
                   0.25 / 0.85, 0.03 / 0.85, 0.2 / 0.85, 0.01 / 0.85,
                   0.04 / 0.85]

        # Maximal difference between required utilization and actual
        # utilization is set to 1 percent:
        threshold = 10.0

        # Create task sets from the generator.
        # Each task is a dictionary.
        print("\tCreate task sets.")
        task_sets_waters = []
        while len(task_sets_waters) < 1:
            task_sets_gen = waters_fs.gen_tasksets(
                1, n_task, req_uti, profile, True, threshold / 100.0, 4, True)
            task_sets_waters.append(task_sets_gen[0])
            # Transform tasks to fit framework structure.
            # Each task is an object of task.
            task_sets_waters.append(task_sets_gen)

        # Transform tasks to fit framework structure.
        # Each task is an object of utilities.task.Task.
        trans5 = trans.Transformer(task_sets_waters, 100)
        task_sets = trans5.transform_tasks(False, n_PE=n_PE, mapping=0)
        return task_sets


    else:
        print("Choose a benchmark")
        return

    # except Exception as e:
    #     print(e)
    #     print("ERROR: task generator")
    #     if debug_flag:
    #         breakpoint()
    #     else:
    #         task_sets = []


def main():
    args = docopt(__doc__, version='0.9.1')
    n_gen = 0
    task_sets = []

    while n_gen != int(args['--nset']):
        task_set = generate_taskset(args)
        n_gen += 1
        task_sets.append(task_set[0])

    ###
    # Save data.
    ###
    print("= Save data =")

    try:
        for ts in task_sets:
            header = ['name', 'offset', 'bcet', 'wcet', 'period', 'deadline']

            with open('out-' + str(task_sets.index(ts)) + '.csv', 'w', encoding='UTF8') as f:
                writer = csv.writer(f)

                # write the header
                writer.writerow(header)

                for t in ts:
                    writer.writerow(t.get_data())

    except Exception as e:
        print(e)
        print("ERROR: save")
        if debug_flag:
            breakpoint()
        else:
            return


if __name__ == '__main__':
    main()
