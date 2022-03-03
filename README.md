
<h1 align="center">
  Real-time Taskset Generator
</h1>
<h4 align="center">A collection of some taskset generators for real-time systems</h4>
<p align="center">
  <a href="https://github.com/porya-gohary/Multi-rate-DAG-Framework/blob/master/LICENSE.md">
    <img src="https://img.shields.io/hexpm/l/apa"
         alt="Gitter">
  </a>
    <img src="https://img.shields.io/badge/Python-3.7+-brightgreen">

</p>
<p align="center">
  <a href="#-dependencies-and-required-packages">Dependencies</a> •
  <a href="#%EF%B8%8F-usage">Usage</a> •
  <a href="#-features">Features</a> •
  <a href="#-limitations">Limitations</a> •
  <a href="#-license">License</a>
</p>
<h4 align="center">NOTICE: THIS PROGRAM IS UNDER DEVELOPMENT...</h4>


## 📦 Required Packages
Assuming that `Python3` is installed in the targeted machine, to install the required packages:
```
pip3 install docopt scipy numpy csv graphviz
```
or
```
python3 -m pip install docopt scipy numpy csv graphviz
```

## ⚙️ Usage
### Task generator:

The options of the taskset generator are as follows (`python3 ./task_generator.py -h`):
```
Usage:
    task_generator                [options]

Options:
    --round, -r                         round the numbers [default: False]
    --utilization=N, -u N               system utilization in percent  [default: 50]
    --generator=N, -g N                 task generation algorithm (0: WATERS 1: UUniFast 2: Emberson 3:WATERS (fixed-sum))  [default: 1]
    --mapping=N, -m N                   the mapping algorithm of taskset (0: No mapping 1: Worst-fit 2: First-fit) [default: 0]
    --ntask=N, -n N                     number of tasks in one taskset  [default: 15]
    --nset=N, -s N                      number of tasksets to generate  [default: 1]
    --npe=N, -p N                       number of processing elements  [default: 4]
    --version, -v                       show version and exit
    --help, -h                          show this message
```
To test the tool and run the taskset generator with the default options:
```
$ python3 ./task_generator.py
```

### Directed acyclic graph (DAG) generator:
The options of the DAG generator are as follows (`python3 ./dag_generator.py -h`):
```
Usage:
    dag_generator               [-t FILE] [options]

Options:
    --taskset FILE, -t FILE          taskset csv file [default: taskset-0.csv]
    --root=N, -r N                   number of root node in graph [default: 5]
    --branch=N, -b N                 branch factor of a node (maximum number of children) [default: 4]
    --depth=N, -d N                  maximum depth of graph [default: 8]
    --version, -v                    show version and exit
    --help, -h                       show this message

```
Assuming that the taskset generated by `./task_generator.py` is named `taskset-0.csv` and present in the current directory, to test the DAG generator with the default options:
```
$ python3 ./dag_generator.py
```
⚠️ NOTE: This DAG generator does not produce fork-join graphs.

#### Output format:
The DAG generator tool works with standard XML format ([Example](./example/taskset-0.xml)). Each XML file contain the following information:
- Task specification:
    * Task name (should start with "T")
    * Best-case execution time (BCET)
    * Worse-case execution time (WCET)
    * Period
    * Deadline
    * Mapped processing element (PE)
- Edge specification
    * Source task
    * Edge name
    * Destination task



## 🔧 Features
  * "[UUnifast](https://dl.acm.org/doi/abs/10.1007/s11241-005-0507-9)" taskset generator<sup>[1](#note1)</sup>
  * "[Real world automotive benchmark for free](https://www.ecrts.org/forum/viewtopic.php?f=20&t=23)" taskset generator with subset sum algorithm<sup>[1](#note1)</sup>
  * "[Emberson et al.](https://www.ecrts.org/archives/fileadmin/WebsitesArchiv/Workshops/WATERS/Proceedings/WATERS-2010-Proceedings.pdf#page=6)" taskset generator
  * "[Real world automotive benchmark for free](https://www.ecrts.org/forum/viewtopic.php?f=20&t=23)" taskset generator with RandFixedSum algorithm
  * Random multi-rate DAG generator<sup>[2](#note2)</sup>

<a name="note1">1</a>: Some part of the code adapted from "[Timing Analysis of Asynchronized Distributed Cause-Effect Chains](https://github.com/tu-dortmund-ls12-rt/end-to-end)" paper implementation

<a name="note2">2</a>: Some part of the code adapted from [here](https://github.com/Spiraline/DAGGen)

## 🚧 Limitations 
- For now, the generators just supports the discrete-time model and all the numbers are integer.

## 🌱 Contribution
With your feedback and conversation, you can assist me in developing this application.
- Open pull request with improvements
- Discuss feedbacks and bugs in issues

## 📜 License
Copyright © 2021 [Pourya Gohari](https://pourya-gohari.ir)

This project is licensed under the Apache License 2.0 - see the [LICENSE.md](LICENSE.md) file for details