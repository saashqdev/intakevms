#!/usr/bin/bash

USER=virtman
DOCS_PROJECT_NAME=intakevms-docs
USER_PATH=/opt/$USER
FOLDER_PATH="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
DOCS_PROJECT_PATH="${USER_PATH}/${DOCS_PROJECT_NAME}"

# Color settings
RED='\033[0;31m'
GREEN='\033[0;32m'
CYAN='\033[0;36m'
NC='\033[0m'

# ========= Common function for checking existence =========
check_existence() {
  local entity_name=$1
  local entity_count=$2

  if [ $entity_count -gt 0 ]; then
    printf ">>>>>> ${CYAN}There are existing entities in your system $entity_name.${NC}\n"
    printf "${CYAN}Continuing to delete will result in loss of all data.${NC}\n"
    printf "${CYAN}What do you want to do next?\n"
    printf "${CYAN}1. Continue deletion.\n"
    printf "${CYAN}2. Stop the removal process.\n${NC}"

    choice=""
    while [ "$choice" != "1" ] && [ "$choice" != "2" ]; do
      read -p "Select action (enter 1 or 2): " choice

      case $choice in
        1) printf "Continue deletion...\n";;
        2) printf "The removal process has stopped.\n"; exit 1;;
        *) printf "${RED}Incorrect input. Please enter 1 or 2.${NC}\n";;
      esac
    done
  else
    printf ">>>>>> ${CYAN}There are no created files in your system. $entity_name.${NC}\n"
  fi
}

# ========= Check Volume existence =========
check_volume_existence() {
  local volume_count=$(sudo docker exec postgres psql -U $USER -d intakevms -t -c "SELECT COUNT(*) FROM volumes;")
  check_existence "virtual disks" $volume_count
}

# ========= Check Image existence =========
check_image_existence() {
  local image_count=$(sudo docker exec postgres psql -U $USER -d intakevms -t -c "SELECT COUNT(*) FROM images;")
  check_existence "virtual images" $image_count
}

# ========= Check Storage existence =========
check_storage_existence() {
  local storage_count=$(sudo docker exec postgres psql -U $USER -d intakevms -t -c "SELECT COUNT(*) FROM storages;")
  check_existence "storage" $storage_count
}

# ========= Check VM existence =========
check_vm_existence() {
  local vm_count=$(sudo docker exec postgres psql -U $USER -d intakevms -t -c "SELECT COUNT(*) FROM virtual_machines;")
  check_existence "virtual machines" $vm_count
}

check_image_existence
check_volume_existence
check_storage_existence
check_vm_existence

# ========= Daemons =========
# Go to home dir of new user
go_to_home_dir(){
  cd /opt/$USER || { printf ">>>>>> ${RED}FAILURE IN GOING TO HOME DIR${NC}\n"; return; }
  printf ">>>>>> ${GREEN}SUCCESSFULLY WENT TO HOME DIR${NC}\n"
}
go_to_home_dir

stop_service(){
  sudo systemctl stop "$1" || { printf ">>>>>> ${RED}FAILURE IN STOPPING SERVICE ${1}${NC}\n"; return; }
  printf ">>>>>> ${GREEN}SUCCESSFULLY STOPPED SERVICE ${1}${NC}\n"
}

disable_service(){
  sudo systemctl disable "$1" || { printf ">>>>>> ${RED}FAILURE IN DISABLING SERVICE ${1}${NC}\n"; return; }
  printf ">>>>>> ${GREEN}SUCCESSFULLY DISABLED SERVICE ${1}${NC}\n"
}

remove_service(){
  sudo rm /etc/systemd/system/"$1" || { printf ">>>>>> ${RED}FAILURE IN REMOVING SERVICE ${1} FROM SYSTEMD/SYSTEM${NC}\n"; return; }
  printf ">>>>>> ${GREEN}SUCCESSFULLY REMOVED SERVICE ${1} FROM SYSTEMD/SYSTEM${NC}\n"
}

restart_service(){
  sudo systemctl restart "$1" || { printf ">>>>>> ${RED}FAILURE IN RESTARTING SERVICE ${1}${NC}\n"; return; }
  printf ">>>>>> ${GREEN}SUCCESSFULLY RESTARTED SERVICE ${1}${NC}\n"
}

for file in $(sudo find /opt/$USER/intakevms/ -name *.service)
do
  stop_service `basename $file`
  disable_service `basename $file`
  remove_service `basename $file`
done

# Removing venv
remove_venv(){
  yes | sudo rm -rf /opt/$USER/intakevms/venv || { printf ">>>>>> ${RED}FAILURE IN REMOVING VENV${NC}\n"; return; }
  printf ">>>>>> ${GREEN}SUCCESSFULLY REMOVED VENV${NC}\n"
}
remove_venv

# Removing built docs
remove_docs(){
  yes | sudo rm -rf /opt/$USER/intakevms/docs/build || { printf ">>>>>> ${RED}FAILURE IN REMOVING DOCS${NC}\n"; return; }
  printf ">>>>>> ${GREEN}SUCCESSFULLY REMOVED DOCS${NC}\n"
}
remove_docs

# Removing libpq-dev
remove_libpq_dev(){
  printf ">>>>>> ${CYAN}REMOVING LIBPQ-DEV${NC}\n"
  yes | sudo apt-get purge libpq-dev || { printf ">>>>>> ${RED}FAILURE IN REMOVING LIBPQ-DEV${NC}\n"; return; }
  printf ">>>>>> ${GREEN}SUCCESSFULLY REMOVED LIBPQ-DEV${NC}\n"
}
remove_libpq_dev

remove_requirements_for_libvirt(){
  printf ">>>>>> ${CYAN}REMOVING REQUIREMENTS FOR LIBVIRT${NC}\n"
  yes | sudo apt remove qemu-kvm libvirt-daemon-system libvirt-clients bridge-utils libvirt-dev || { printf ">>>>>> ${RED}FAILURE IN REMOVING REQUIREMENTS FOR LIBVIRT${NC}\n"; return; }
  printf ">>>>>> ${GREEN}SUCCESSFULLY REMOVED REQUIREMENTS FOR LIBVIRT${NC}\n"
}
remove_requirements_for_libvirt

# Removing PostgreSQL Docker
remove_postgresql_docker(){
  sudo docker stop postgres || { printf ">>>>>> ${RED}FAILURE IN STOPPING POSTGRESQL DOCKER${NC}\n"; return; }
  sudo docker rm postgres || { printf ">>>>>> ${RED}FAILURE IN REMOVING POSTGRESQL DOCKER${NC}\n"; return; }
  printf ">>>>>> ${GREEN}SUCCESSFULLY REMOVED POSTGRESQL DOCKER${NC}\n"
}
remove_postgresql_docker

# Removing RabbitMQ Docker
remove_rabbitmq_docker(){
  sudo docker stop rabbit || { printf ">>>>>> ${RED}FAILURE IN STOPPING RABBITMQ DOCKER${NC}\n"; return; }
  sudo docker rm rabbit || { printf ">>>>>> ${RED}FAILURE IN REMOVING RABBITMQ DOCKER${NC}\n"; return; }
  printf ">>>>>> ${GREEN}SUCCESSFULLY REMOVED RABBITMQ DOCKER${NC}\n"
}
remove_rabbitmq_docker

# Removing Prometheus and NodeExporter
remove_prometheus_folders(){
  sudo rm -rf /var/db/prometheus || { printf ">>>>>> ${RED}FAILURE IN REMOVING PROMETHEUS FOLDERS${NC}\n"; return; }
  sudo rm -rf /etc/prometheus || { printf ">>>>>> ${RED}FAILURE IN REMOVING PROMETHEUS FOLDERS${NC}\n"; return; }
  sudo rm -rf /usr/local/bin/prometheus || { printf ">>>>>> ${RED}FAILURE IN REMOVING PROMETHEUS FOLDERS${NC}\n"; return; }
  sudo rm -rf /usr/local/bin/promtool || { printf ">>>>>> ${RED}FAILURE IN REMOVING PROMETHEUS FOLDERS${NC}\n"; return; }
  printf ">>>>>> ${GREEN}SUCCESSFULLY REMOVED ALL FOLDERS FOR PROMETHEUS${NC}\n"
}
remove_prometheus_folders

stop_service "prometheus.service"
disable_service "prometheus.service"
remove_service "prometheus.service"

remove_node_exporter_folders(){
  sudo rm -rf /usr/local/bin/node_exporter || { printf ">>>>>> ${RED}FAILURE IN REMOVING NODE_EXPORTER FOLDERS${NC}\n"; return; }
  printf ">>>>>> ${GREEN}SUCCESSFULLY REMOVED ALL FOLDERS FOR NODE_EXPORTER${NC}\n"
}
remove_node_exporter_folders

stop_service "node_exporter.service"
disable_service "node_exporter.service"
remove_service "node_exporter.service"

remove_novnc_folder(){
  sudo rm -rf /opt/virtman/intakevms/intakevms/libs/noVNC || { printf ">>>>>> ${RED}FAILURE IN REMOVING NOVNC FOLDER${NC}\n"; return; }
  printf ">>>>>> ${GREEN}SUCCESSFULLY REMOVED NOVNC FOLDER${NC}\n"
}
remove_novnc_folder

remove_nodejs_folders(){
  sudo rm -rf /usr/local/lib/nodejs
  sudo rm -rf /usr/local/include/node
  sudo rm /usr/local/bin/node
  sudo rm /usr/local/share/man/man1/node.1
  sudo rm /usr/local/lib/dtrace/node.d
  sudo rm /usr/local/bin/npm
  sudo rm /usr/local/share/man/man1/npm.1
  sudo rm -rf ~/.npm

  sudo ls -la /usr/local/bin | grep "node"
  sudo rm -rf /usr/local/bin/npm
  sudo rm -rf /usr/local/bin/node
  sudo rm -rf /usr/local/bin/npx

  printf ">>>>>> ${GREEN}SUCCESSFULLY REMOVED ALL FOLDERS FOR NODEJS${NC}\n"
}
remove_nodejs_folders

# ========= Unmount directories =========
umount_project_paths(){
  sudo umount -l /opt/virtman/intakevms/data/mnt/*
}
umount_project_paths

# ========= Remove project folder =========
remove_project_folder(){
  # Checking if a folder exists
  if [ -d "$FOLDER_PATH" ]; then
      # Executing the command to delete a folder
      sudo rm -rf "$FOLDER_PATH"
      echo "Folder $FOLDER_PATH successfully deleted."
  else
      echo "Folder $FOLDER_PATH not found."
  fi
}
remove_project_folder

remove_documentation_repository(){
  if [ -d "$DOCS_PROJECT_PATH" ]; then
      sudo rm -rf "$DOCS_PROJECT_PATH"
      echo "Folder $DOCS_PROJECT_PATH successfully deleted."
  else
      echo "Folder $DOCS_PROJECT_PATH not found."
  fi
}
remove_documentation_repository

restart_service "cups-browsed.service"
restart_service "cups.service"
restart_service "NetworkManager.service"
restart_service "packagekit.service"
restart_service "systemd-resolved.service"
restart_service "user@1000.service"
