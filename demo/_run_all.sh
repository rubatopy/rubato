# Use ctrl+z to stop the script. ctrl+c won't work.
# Run it from the demo folder with: ./_run_all.sh
# Does not work if you run it from outside the demo folder.

files=`ls ./*.py`

PYCOMMAND=python

for file in $files
do
    echo "Running $file"
    timeout --preserve-status 5s $PYCOMMAND $file
    retVal=$?
    echo $retVal
    if [ "$retVal" != "143"  ] && [ "$retVal" != "124" ]
    then
        exit 1
    fi
done
