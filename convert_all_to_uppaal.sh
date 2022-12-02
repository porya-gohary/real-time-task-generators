mkdir -p ./uppaal_xml
for file in ./tasksets/taskset-*.csv ; do
    echo ${file}
    python3 task_set_to_uppaal.py -t ${file}
    mv taskset-*.xml ./uppaal_xml
    mv taskset-*.q ./uppaal_xml
done