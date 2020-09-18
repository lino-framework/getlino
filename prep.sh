set -e  # exit on error
# delete all stopped containers?
# docker container prune
# docker system prune

# needed only the first time?
docker build -t debian_updated -f Dockerfiles/debian_updated .
docker build -t ubuntu_updated -f Dockerfiles/ubuntu_updated .

docker build -t debian_with_getlino -f Dockerfiles/debian_with_getlino .
docker build -t ubuntu_with_getlino -f Dockerfiles/ubuntu_with_getlino .

# docker build -t getlino_ubuntu -f Dockerfiles/ubuntu .
# docker build --no-cache -t getlino_debian -f Dockerfiles/debian .
# docker build --no-cache -t getlino_ubuntu -f Dockerfiles/ubuntu .
