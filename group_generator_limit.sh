#!/bin/bash
help="
Usage:
      group_generator_test.sh  [-argument value]...

Options:
    -s N                      number of tasksets to generate  [default: 1]
    -n N                      number of tasks in each taskset  [default: 10]
    -u N                      system utilization in percent  [default: 50]
    -g N                      task generation algorithm (0: WATERS 1: UUniFast 2: Emberson 3: WATERS (fixed-sum))  [default: 1]
    -p N                      priority assigning method (0: Rate-monotonic 1: Deadline-monotonic 2: Earliest deadline first (EDF)) [default: 0]
    -c N                      number of cores [default: 4]
    -v                        show version and exit
    -h                        show this message
"
version="group_generator_test.sh 0.6.0"
n_tasksets=1
utilization=50
algorithm=1
priority=0
cores=4
n_tasks=10
n_jobs_limit=10001
while getopts "s:n:u:g:p:c:vh" opt; do
  case $opt in
  s)
    n_tasksets=$OPTARG
    ;;
  n)
    n_tasks=$OPTARG
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

# generate tasksets one by one and run the test
mkdir -p ./tasksets
mkdir -p ./jobsets
i=0
while [ $i -lt $n_tasksets ]; do
    echo "Generating taskset $i"
    # generate taskset and jobset until the number of jobs is less than the limit
    while true; do
      python3 task_generator.py -s 1 -u $utilization -g $algorithm -p $cores -n $n_tasks
      # run for 1 minute max
      exit_code=$(timeout 1m python3 priority_generator.py -t ./taskset-0.csv -m $priority -s)
      if [[ $exit_code -eq 124 ]]; then
        echo "[!] job set generation timeout"
        continue
      fi
      #python3 priority_generator.py -t ./taskset-0.csv -m $priority -s
      # count number of line in the jobset file
      n_jobs=$(wc -l < ./jobset-taskset-0.csv)
      if [ $n_jobs -lt $n_jobs_limit ]; then
        break
      else
        echo "[!] too many jobs, regenerating task set"
      fi
    done    
     mv taskset-*.csv ./tasksets/taskset-$i.csv
     mv jobset-*.csv ./jobsets/jobset-taskset-$i.csv
     i=$((i+1))
done


