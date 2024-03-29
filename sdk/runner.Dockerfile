ARG BASE_IMAGE=eidolonai/sdk:latest
FROM ${BASE_IMAGE}
RUN addgroup --system --gid 1001 eidolon
RUN adduser --system --uid 1001 eidolon
USER eidolon
EXPOSE 8080
ENV PYTHONUNBUFFERED 1
# todo: we expect resources to be mounted somewhere, mount/resources;
# todo: we likely want to add "mount" to the python path so that we can also add python custmization there as well
WORKDIR app
CMD eidolon-server resources