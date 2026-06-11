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
  apt-get install -y --no-install-recommends libmagic1 build-essential libmagic-dev
  pip install --upgrade pip
  pip install -r requirements.txt
  apt-get remove --autoremove -y build-essential libmagic-dev
  rm -rf /var/lib/apt/lists/*
EOF

# Copy project
COPY ./entrypoint.sh /
COPY ./app /app/

# Compile translations at build time without keeping gettext in the runtime image.
RUN <<EOF
  set -exo pipefail
  apt-get update
  apt-get install -y --no-install-recommends gettext
  mkdir -p /logging
  SECRET_KEY=build-only-secret-key python manage.py compilemessages
  apt-get purge --autoremove -y gettext
  rm -rf /var/lib/apt/lists/*
EOF

# Run the application
ENTRYPOINT ["bash", "/entrypoint.sh"]
