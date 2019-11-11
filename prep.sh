# docker build -t dev docker/dev
# docker build -t contrib -f docker/contrib/Dockerfile .
docker build --no-cache -t prod_debian  -f docker/prod/Dockerfile .
docker build --no-cache -t prod_ubuntu  -f docker/prod/Dockerfile_ubuntu .
