#!/bin/bash

USER=virtman
OS=$(cat /etc/issue)
ARCH=$(arch)

# Project settings
PROJECT_NAME=intakevms
USER_PATH=/opt/$USER
PROJECT_PATH="${USER_PATH}/${PROJECT_NAME}"
DEPENDENCIES_FILE="${PROJECT_PATH}/third_party_requirements.txt"

# Color settings
RED='\033[0;31m'
GREEN='\033[0;32m'
CYAN='\033[0;36m'
NC='\033[0m'

#===================== GIT MANAGER =================
# Checking for jq utility availability
if ! command -v jq &> /dev/null; then
    echo "The jq utility is not installed. Install it for the script to work.."
    exit 1
fi

# Set up variables for the GitHub repository and API
REPO_OWNER="OWNER_NAME"
REPO_NAME="REPO_NAME"
API_URL="https://api.github.com/repos/$REPO_OWNER/$REPO_NAME/branches"

# Getting a list of branches using the GitHub API
branches=$(curl -s "$API_URL")
version_branches=()

# Function to check if a branch name matches the x.x.x mask
function is_version_branch {
    [[ $1 =~ ^[0-9]+\.[0-9]+\.[0-9]+$ ]]
}

# Function to update alembic migrations
update_migrations(){
  message="FAILURE IN UPDATING ALEMBIC MIGRATIONS"
  sudo alembic upgrade head || { show_alert_message "$message"; return; }
  printf ">>>>>> ${GREEN}SUCCESSFULLY UPDATED ALEMBIC MIGRATIONS${NC}\n"
}

while IFS= read -r branch; do
    if is_version_branch "$branch"; then
        version_branches+=("$branch")
    fi
done < <(echo "$branches" | jq -r '.[].name')

# We pull up new branches, if there are any
git pull

# List matching branch names
echo "Available versions for update:"

select branch in "${version_branches[@]}"; do
    if [ -n "$branch" ]; then
        echo "You have selected a branch: $branch"
        git checkout "$branch"
        echo "Applying Alembic Migrations to a New Branch: $branch"
        update_migrations
        break
    else
        echo "Invalid selection. Please select a branch number from the list."
    fi
done

show_alert_message() {
  local message=$1
  
  printf ">>>>>> ${RED}$message${NC}\n"
  error_messages+=("${RED}ERROR:${NC} $message")
}

# Go to home dir of new user
go_to_home_dir(){
  message="FAILURE IN GOING TO HOME DIR"
  cd $USER_PATH || { show_alert_message "$message"; return; }
  printf ">>>>>> ${GREEN}SUCCESSFULLY WENT TO HOME DIR${NC}\n"
}

# ========= FUNCTIONS FOR DAEMONS =========

add_service(){
  message="FAILURE IN ADDING SERVICE ${1} TO SYSTEMD/SYSTEM"
  sudo cp "$1" /etc/systemd/system/ || { show_alert_message "$message"; return; }
  printf ">>>>>> ${GREEN}SUCCESSFULLY ADDED SERVICE ${1} TO SYSTEMD/SYSTEM${NC}\n"
}

enable_service(){
  message="FAILURE IN ENABLING SERVICE ${1}"
  sudo systemctl enable "$1" || { show_alert_message "$message"; return; }
  printf ">>>>>> ${GREEN}SUCCESSFULLY ENABLED SERVICE ${1}${NC}\n"
}

start_service(){
  message="FAILURE IN STARTING SERVICE ${1}"
  sudo systemctl start "$1" || { show_alert_message "$message"; return; }
  printf ">>>>>> ${GREEN}SUCCESSFULLY STARTED SERVICE ${1}${NC}\n"
}

restart_service(){
  message="FAILURE IN RESTARTING SERVICE ${1}"
  sudo systemctl restart "$1" || { show_alert_message "$message"; return; }
  printf ">>>>>> ${GREEN}SUCCESSFULLY RESTARTED SERVICE ${1}${NC}\n"
}

# Main script
go_to_home_dir

for file in $(sudo find $PROJECT_PATH/ -name *.service)
do
  add_service "$file"
  enable_service `basename $file`
  restart_service `basename $file`
done
