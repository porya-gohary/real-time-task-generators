"""Transform task from dictionaries to task objects for the event simulator.
Some part adapted from https://github.com/tu-dortmund-ls12-rt/end-to-end
"""
import lib.task as t
from scipy import stats


class Transformer:
    """Transformer class."""

    def __init__(self, t_task_sets, time_scale=10000000):
        """Creates a transformer object."""
        self.task_sets = t_task_sets  # task set as dictionary
        self.time_scale = time_scale  # scaling factor for period, WCET, etc.

    def transform_tasks(self, phase, n_PE=1, mapping=0):
        """Transform the given tasks.
        The flag phase specifies if phases should be introduced to the task
        set.
        - set phase
        - number of PE
        - mapping policy (0 -> not changing, 1 -> worst-fit, 2 -> first-fit , 3 -> best-fit [Not implemented yet])
        """
        # Distribution of task phases
        distribution_phase = stats.uniform()

        # Initialization of the transformed task sets
        transformed_task_sets = []
        PE_util = [1] * n_PE
        for task_set in self.task_sets:
            # Sort tasks set by periods.
            sorted_task_set = sorted(task_set, key=lambda task: task.period)
            transformed_task_set = []
            i = 0
            # Transform each task individually.
            for task in sorted_task_set:
                # Set phase.
                if phase:
                    phase = int(float(format(distribution_phase.rvs() * 1000,
                                             ".2f")) * self.time_scale)
                else:
                    phase = 0
                # Scale values and make a task object.
                if (mapping == 0):
                    transformed_task_set.append(
                        t.task(name='T' + str(i), phase=phase,
                               wcet=(int(float(format(task.wcet, ".2f"))
                                         * self.time_scale)
                                     if int(float(format(task.wcet, ".2f"))
                                            * self.time_scale) else int(float(format(task.wcet, ".2f"))
                                                                        * self.time_scale) + 1),
                               period=int(float(format(task.period, ".2f"))
                                          * self.time_scale),
                               pe=task.pe,
                               deadline=int(float(format(task.deadline, ".2f"))
                                            * self.time_scale)))
                elif (mapping == 1):
                    max_index = PE_util.index(max(PE_util))
                    u = (task.wcet / task.period)
                    task.pe = max_index
                    PE_util[task.pe] -= u
                    transformed_task_set.append(
                        t.task(name='T' + str(i), phase=phase,
                               wcet=(int(float(format(task.wcet, ".2f"))
                                         * self.time_scale)
                                     if int(float(format(task.wcet, ".2f"))
                                            * self.time_scale) else int(float(format(task.wcet, ".2f"))
                                                                        * self.time_scale) + 1),
                               period=int(float(format(task.period, ".2f"))
                                          * self.time_scale),
                               pe=task.pe,
                               deadline=int(float(format(task.deadline, ".2f"))
                                            * self.time_scale)))
                elif (mapping == 2):
                    first_index = 0
                    u = (task.wcet / task.period)
                    for i in range (n_PE):
                        if (PE_util[first_index]- u >= 0):
                            break
                        first_index+=1
                    task.pe = first_index
                    PE_util[task.pe] -= u
                    transformed_task_set.append(
                        t.task(name='T' + str(i), phase=phase,
                               wcet=(int(float(format(task.wcet, ".2f"))
                                         * self.time_scale)
                                     if int(float(format(task.wcet, ".2f"))
                                            * self.time_scale) else int(float(format(task.wcet, ".2f"))
                                                                        * self.time_scale) + 1),
                               period=int(float(format(task.period, ".2f"))
                                          * self.time_scale),
                               pe=task.pe,
                               deadline=int(float(format(task.deadline, ".2f"))
                                            * self.time_scale)))
                i += 1
            transformed_task_sets.append(transformed_task_set)
        return transformed_task_sets
