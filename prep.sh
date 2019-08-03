# docker build -t dev docker/dev
# docker build -t contrib -f docker/contrib/Dockerfile .
docker build -t prod  -f docker/prod/Dockerfile .
