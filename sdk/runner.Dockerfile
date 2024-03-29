ARG BASE_IMAGE=eidolonai/sdk:latest
FROM ${BASE_IMAGE}
RUN addgroup --system --gid 1001 eidolon
RUN adduser --system --uid 1001 eidolon
USER eidolon
EXPOSE 8080
ENV PYTHONUNBUFFERED 1
WORKDIR app
ENTRYPOINT ["eidolon-server"]
CMD ["resources"]