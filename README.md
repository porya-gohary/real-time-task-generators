
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
pip3 install docopt scipy numpy csv
```
or
```
python3 -m pip install docopt scipy numpy csv
```

## ⚙️ Usage
The options of the taskset generator are as follows (`python3 ./main.py -h`):
```
Usage:
    main                [options]

Options:
    --round, -r             round the numbers [default: False]
    --utilization=N, -u N   system utilization in percent  [default: 50]
    --generator=N, -g N     task generation algorithm (0: WATERS 1: UUniFast 2: Emberson 3:WATERS (fixed-sum))  [default: 1]
    --ntask=N, -n N         number of tasks in one taskset  [default: 15]
    --nset=N, -s N          number of tasksets to generate  [default: 1]
    --npe=N, -m N           number of processing elements  [default: 4]
    --version, -v           show version and exit
    --help, -h              show this message
```
To test the tool and run the taskset generator with the default options:
```
$ python3 ./main.py
```

## 🔧 Features
- Taskset Generator:
  * "[UUnifast](https://dl.acm.org/doi/abs/10.1007/s11241-005-0507-9)" taskset generator<sup>[1](#note1)</sup>
  * "[Real world automotive benchmark for free](https://www.ecrts.org/forum/viewtopic.php?f=20&t=23)" taskset generator with subset sum algorithm<sup>[1](#note1)</sup>
  * "[Emberson et al.](https://www.ecrts.org/archives/fileadmin/WebsitesArchiv/Workshops/WATERS/Proceedings/WATERS-2010-Proceedings.pdf#page=6)" taskset generator
  * "[Real world automotive benchmark for free](https://www.ecrts.org/forum/viewtopic.php?f=20&t=23)" taskset generator with RandFixedSum algorithm


<a name="note1">1</a>: Some part of the code adabted from "[Timing Analysis of Asynchronized Distributed Cause-Effect Chains](https://github.com/tu-dortmund-ls12-rt/end-to-end)" paper implementation

## 🚧 Limitations 
- For now, the generators just supports the discrete-time model and all the numbers are integer.
## 📜 License
Copyright © 2021 [Pourya Gohari](https://pourya-gohari.ir)

This project is licensed under the Apache License 2.0 - see the [LICENSE.md](LICENSE.md) file for details