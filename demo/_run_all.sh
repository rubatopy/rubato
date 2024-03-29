# Use ctrl+z to stop the script. ctrl+c won't work.
# Run it from the demo folder with: ./_run_all.sh
# Does not work if you run it from outside the demo folder.

files=`ls ./*.py && ls ./platformer/main.py`

BLUE='\033[1;34m'
NC='\033[0m' # No Color

ogdir="$( pwd )"

for file in $files
do
    printf "${BLUE}Running $file${NC}\n"
    cd "$( dirname "$file" )"
    if command -v python &> /dev/null
    then
        timeout --preserve-status --foreground 5s python "$(basename $file)"
    else
        timeout --preserve-status --foreground 5s python3 "$(basename $file)"
    fi

    retVal=$?
    if [ "$retVal" != "143"  ] && [ "$retVal" != "124" ] && [ "$retVal" != "0" ]
    then
        exit 1
    elif [ "$retVal" == "130" ]
    then
        exit 1
    fi
done

cd $ogdir
