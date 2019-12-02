set -e  # exit on error
docker build --no-cache -t getlino_debian  -f docker/prod/Dockerfile .
#docker build --no-cache -t getlino_ubuntu  -f docker/prod/Dockerfile_ubuntu .
