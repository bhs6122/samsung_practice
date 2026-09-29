FROM ubuntu:24.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-venv \
    openssh-server \
    ca-certificates \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

RUN useradd -m -s /bin/bash dev \
    && mkdir -p /run/sshd /home/dev/workspace \
    && chown -R dev:dev /home/dev/workspace

RUN printf 'PasswordAuthentication yes\nPermitRootLogin no\n' \
    > /etc/ssh/sshd_config.d/00-dev.conf

WORKDIR /home/dev/workspace

EXPOSE 22

CMD ["/bin/sh", "-c", "ssh-keygen -A && exec /usr/sbin/sshd -D -e"]
