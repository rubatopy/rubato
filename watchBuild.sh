BLUE='\033[1;34m'
NC='\033[0m' # No Color

make build

OLD_TAIL=$(cat rubato/**/*.py)

printf "${BLUE}Waiting for changes...${NC}\n"

while true; do
    NEW_TAIL=$(cat rubato/**/*.py)
    if [ "$OLD_TAIL" != "$NEW_TAIL" ]; then
        printf "${BLUE}Rebuilding...${NC}\n"
        make build
        OLD_TAIL=$NEW_TAIL
        printf "${BLUE}Waiting for changes...${NC}\n"
    fi
    sleep 1
done
