FROM alpine:3.12.0

# Install python
RUN apk add linux-headers
RUN apk add -y --update gcc python3 python3-dev py3-pip musl-dev libwebsockets-dev
# Copy requirements.txt
COPY requirements.txt /tmp/requirements.txt
RUN pip3 --version

# Install requirements
RUN pip3 install -r /tmp/requirements.txt
# Remove requirements.txt
RUN rm /tmp/requirements.txt
# Remove dependencies
RUN apk del gcc python3-dev musl-dev py3-pip linux-headers
# Remove cache
RUN rm -rf /var/cache/apk/*


# Set working directory
WORKDIR /app

# Copy contents
COPY . /app


# EXPOSE port 3000 & 7681
EXPOSE 3000
EXPOSE 7681

# Executable ttyd.x86_64
RUN chmod +x /app/ttyd.x86_64

# ENTRYPOINT
CMD [ "/bin/sh", "-c", "/app/ttyd.x86_64 -W -w ~ /bin/sh \
            & python3 /app/app.py" ]