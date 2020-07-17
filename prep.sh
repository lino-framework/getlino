set -e  # exit on error
# delete all stopped containers:
# docker container prune
docker build --no-cache -t getlino_debian -f Dockerfiles/debian .
# docker build --no-cache -t getlino_ubuntu -f Dockerfiles/ubuntu .
