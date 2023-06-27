# -- build stager --
FROM python:3.10-alpine3.18 AS build

# -- deps upgrades and installation --
RUN apk add -y --update --no-cache gcc python3 python3-dev py3-pip musl-dev linux-headers
RUN python3 -m ensurepip --upgrade && python3 -m pip install pex~=2.1.47

# -- build pex from deps --
RUN mkdir /source
COPY requirements.txt /source/
RUN pex -r /source/requirements.txt -o /source/pex_wrapper

# -- release stager --
FROM python:3.10-alpine3.18 AS final
RUN apk upgrade --no-cache

# -- copy from build stage --
WORKDIR /app
COPY . /app
COPY --from=build /source /app/

# -- app setup --
EXPOSE 3000
EXPOSE 7681
RUN chmod +x /app/ttyd.x86_64

# -- startup command --
CMD [ "/bin/sh", "-c", "/app/ttyd.x86_64 -w ~ /bin/sh \
            & /app/pex_wrapper /app/app.py" ]