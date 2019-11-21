if [[ -z "${DOCKER_ELK_REPO_PATH}" ]]; then
  echo "DOCKER_ELK_REPO_PATH env is not set."
else
  # envvar set
  cd ${DOCKER_ELK_REPO_PATH}
  sudo docker-compose down -v
  # sudo docker-compose build
  sudo docker-compose up
fi