if [[ -z "${DOCKER_ELK_REPO_PATH}" ]]; then
  echo "DOCKER_ELK_REPO_PATH env is not set."
else
  # envvar set
  cd ${DOCKER_ELK_REPO_PATH}
  pwd
  sudo docker-compose build
  sudo docker-compose up
fi