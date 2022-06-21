# Use ctrl+z to stop the script. ctrl+c won't work.

files=`ls ./*.py`

PYCOMMAND=python

for file in $files
do
    echo "Running $file"
    timeout --preserve-status 5s $PYCOMMAND $file
    retVal=$?
    if [ "$retVal" != "143" ]
    then
        exit 1
    fi
done
