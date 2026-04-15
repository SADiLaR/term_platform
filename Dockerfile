# A minimalist image usable as a base for a production deployment.
FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

SHELL ["/bin/bash", "-c"]

# Set work directory
WORKDIR /app

# Install dependencies
COPY requirements.txt /app/

RUN <<EOF
  set -exo pipefail
  apt-get update
  apt-get -y upgrade
  apt-get install -y --no-install-recommends libmagic1 gettext gcc libmagic-dev
  pip install --upgrade pip
  pip install -r requirements.txt
  apt-get remove gcc libmagic-dev
  rm -rf /var/lib/apt/lists/*
EOF

# Copy project
COPY ./entrypoint.sh /
COPY ./app /app/

# Run the application
ENTRYPOINT ["bash", "/entrypoint.sh"]
