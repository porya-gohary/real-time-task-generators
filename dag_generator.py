#!/usr/bin/env python3
"""
DAG generator for a specific taskset

Usage:
    dag_generator               [-t FILE] [options]

Options:
    --taskset FILE, -t FILE          taskset csv file [default: taskset-0.csv]
    --root=N, -r N                   number of root node in graph [default: 5]
    --branch=N, -b N                 branch factor of a node (maximum number of children) [default: 4]
    --depth=N, -d N                  maximum depth of graph [default: 8]
    --version, -v                    show version and exit
    --help, -h                       show this message
"""
import sys
import os
from math import ceil, floor, gcd
from random import randint
from lxml import etree as ET
import lib.task as task
import re
import graphviz
from docopt import docopt
import csv


## calculate least common multiple of two number
def lcm(a, b):
    return abs(a * b) // gcd(a, b) if a and b else 0


## calculate hyperperiod of a taskset
def hyperperiod(periods):
    h = 1
    for p in periods:
        h = lcm(h, p)
    return h


def generateDAG(task_set, root_node_num, branch_factor, depth, dag_name):
    """ Generate DAG for a specific task set.
    Variables:
    task_set: Input task set
    branch_factor: maximum number of children at each node
    root_node_num: number of root node in the DAG
    depth: number of DAG level
    """
    ### 0. check number of tasks
    if (len(task_set) < root_node_num + depth):
        print("Small number of task for DAG!")
        return False;

    ### 1. Classify Task by randomly-select level
    level_arr = []
    for i in range(depth):
        level_arr.append([])

    ## put start nodes in level 0
    for i in range(root_node_num):
        level_arr[0].append(i)
        task_set[i].level = 0

    ## Each level must have at least one node
    for i in range(1, depth):
        level_arr[i].append(root_node_num + i - 1)
        task_set[root_node_num + i - 1].level = i

    ## put other nodes in other level randomly
    for i in range(root_node_num + depth - 1, len(task_set)):
        level = randint(1, depth - 1)
        task_set[i].level = level
        level_arr[level].append(i)

    ### 2. Make edges
    for level in range(0, depth - 1):
        for task_idx in level_arr[level]:
            ob_num = randint(0, branch_factor)

            child_idx_list = []

            # if desired outbound edge number is larger than the number of next level nodes, select every node
            if ob_num >= len(level_arr[level + 1]):
                child_idx_list = level_arr[level + 1]
            else:
                while len(child_idx_list) < ob_num:
                    child_idx = level_arr[level + 1][randint(0, len(level_arr[level + 1]) - 1)]
                    if child_idx not in child_idx_list:
                        child_idx_list.append(child_idx)

            for child_idx in child_idx_list:
                task_set[task_idx].child.append(child_idx)
                task_set[child_idx].parent.append(task_idx)

    ### 3. Write to xml file
    root = ET.Element("mrdag", name=dag_name)
    for t in task_set:
        task = ET.SubElement(root, "task", name=t.name)

        spec = ET.SubElement(task, "spec", name="BCET").text = str(t.bcet)
        spec = ET.SubElement(task, "spec", name="WCET").text = str(t.wcet)
        spec = ET.SubElement(task, "spec", name="Period").text = str(t.period)
        spec = ET.SubElement(task, "spec", name="Deadline").text = str(t.deadline)
        spec = ET.SubElement(task, "spec", name="PE").text = str(t.pe)
    edges = ET.SubElement(root, "edges")
    for t in task_set:
        t_num = re.split('(\d+)', t.name)[1]  # get label of source task
        if (len(t.child)):
            for e in t.child:
                edge = ET.SubElement(edges, "edge", srcTask=t.name, name='e' + str(t_num) + ',' + str(e),
                                     dstTask='T' + str(e))
    tree = ET.ElementTree(root)
    tree.write(dag_name + ".xml", xml_declaration=True, encoding='utf-8', pretty_print=True)

    ### 4. Write to dot file (GraphViz)
    G = graphviz.Digraph(name=dag_name, filename=dag_name + ".dot")
    G.attr('node', fontname='Ubuntu')
    # G.attr(dpi=str(300))
    for t in task_set:
        G.node(t.name)
        for e in t.child:
            G.edge(t.name, str("T" + str(e)))
    G.render(format='png')
    G.render(format='svg')

    return True


def read_csv(file):
    taskset = []
    try:
        with open(file, 'r') as read_obj:
            # csv_reader = csv.reader(read_obj)
            csv_dict_reader = csv.DictReader(read_obj)
            # Iterate over each row in the csv using reader object and make tasks
            for row in csv_dict_reader:
                taskset.append(
                    task.task(name=row['Name'], phase=int(row['Offset']), bcet=int(row['BCET']), wcet=int(row['WCET']),
                              period=int(row['Period']), deadline=int(row['Deadline']), pe=int(row['PE'])))
        return taskset
    except Exception as e:
        print(e)
        print("ERROR: reading taskset is not possible")
        sys.exit(1)


def main():
    args = docopt(__doc__, version='0.7.2')
    task_set = read_csv(args['--taskset'])
    dag_name = os.path.splitext(os.path.basename(args['--taskset']))[0]
    generateDAG(task_set=task_set, root_node_num=int(args['--root']), branch_factor=int(args['--branch']),
                depth=int(args['--depth']),
                dag_name=dag_name)
    # print(dag_name)


if __name__ == '__main__':
    main()
