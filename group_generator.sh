#!/bin/bash
help="
Usage:
      group_generator.sh  [-argument value]...

Options:
    -s N                      number of tasksets to generate  [default: 1]
    -u N                      system utilization in percent  [default: 50]
    -g N                      task generation algorithm (0: WATERS 1: UUniFast 2: Emberson 3: WATERS (fixed-sum))  [default: 1]
    -p N                      priority assigning method (0: Rate-monotonic 1: Deadline-monotonic 2: Earliest deadline first (EDF)) [default: 0]
    -c N                      number of cores [default: 4]
    -v                        show version and exit
    -h                        show this message
"
version="group_generator.sh 1.0.0"
n_tasksets=1
utilization=50
algorithm=1
priority=0
cores=4
while getopts "s:u:g:p:c:vh" opt; do
  case $opt in
  s)
    n_tasksets=$OPTARG
    ;;
  u)
    utilization=$OPTARG
    ;;
  g)
    algorithm=$OPTARG
    ;;
  p)
    priority=$OPTARG
    ;;
  c)
    cores=$OPTARG
    ;;
  v)
    echo $version
    exit 0
    ;;
  h)
    echo "$help"
    exit 0
    ;;
  \?)
    echo "Invalid option: -$OPTARG" >&2
    exit 1
    ;;
  :)
    echo "Option -$OPTARG requires an argument." >&2
    exit 1
    ;;
  esac
done

python3 task_generator.py -s $n_tasksets -u $utilization -g $algorithm -p $cores
mkdir -p ./tasksets
mv taskset-*.csv ./tasksets

for file in ./tasksets/taskset-*.csv ; do
    echo ${file}
    python3 priority_generator.py -t ${file} -m $priority -s
done
mkdir -p ./jobsets
mv jobset-*.csv ./jobsets

mkdir -p segmentsets
for file in ./jobsets/jobset-*.csv ; do
    echo ${file}
    python3 job_set_to_segment_set.py -j ${file}
done

mv ./jobsets/jobset-*.yaml ./segmentsets

