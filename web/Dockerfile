FROM alpine

# Initialize
RUN mkdir -p /data/web
WORKDIR /data/web
COPY requirements.txt /data/web/

ENV PACKAGES="\
  python3 \
  python3-dev \
  postgresql-client \
  postgresql-dev \
  build-base \
  gettext \
  gdal-dev \
  py-gdal \
  gdal \
  geos \
"

RUN echo \
  # Replacing default repositories with edge ones
  && echo "http://dl-cdn.alpinelinux.org/alpine/edge/testing" > /etc/apk/repositories \
  && echo "http://dl-cdn.alpinelinux.org/alpine/edge/community" >> /etc/apk/repositories \
  && echo "http://dl-cdn.alpinelinux.org/alpine/edge/main" >> /etc/apk/repositories \
  # Add the packages, with a CDN-breakage fallback if needed
  && apk add --no-cache $PACKAGES || \
    (sed -i -e 's/dl-cdn/dl-4/g' /etc/apk/repositories && apk add --no-cache $PACKAGES)

# Setup Python deps
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

# Prepare
COPY . /data/web/
RUN mkdir -p lizard/static/admin
