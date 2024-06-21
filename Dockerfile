# A minimalist image usable as a base for a production deployment.
FROM python:3.12

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
  apt-get install -y --no-install-recommends libmagic1 gettext
  pip install --upgrade pip
  pip install -r requirements.txt
EOF

# Copy project
COPY ./app /app/
COPY ./entrypoint.sh /

# Run the application
ENTRYPOINT ["bash", "/entrypoint.sh"]
