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
    python3 task_generator.py -s 1 -u $utilization -g $algorithm -p $cores -n $n_tasks
    python3 priority_generator.py -t ./taskset-0.csv -m $priority -s
    # run SAG for the worst case test and get the output
    echo "Running SAG for the worst case test"
    result=$(./test/nptest ./jobset-taskset-0.csv -m $cores -w)
    IFS=',' read -ra result_array <<< "$result"
    # remove additional spaces
    result_array[1]=$(echo "${result_array[1]}" | tr -d '[:space:]')
    echo "SAG result: ${result_array[1]}"
    # if the result is 1, then the test succeeded
    if [ "${result_array[1]}" == "1" ]; then
      echo "Test succeeded"
      mv taskset-*.csv ./tasksets/taskset-$i.csv
      mv jobset-*.csv ./jobsets/jobset-taskset-$i.csv
      i=$((i+1))
    else
      # remove the taskset and jobset files
      rm taskset-*.csv
      rm jobset-*.csv
    fi
done


