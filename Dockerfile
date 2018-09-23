# http://container-solutions.com/6-dockerfile-tips-official-images/
FROM ubuntu:18.04
MAINTAINER 'unkonwn' unkonwn@unkonwn.com
WORKDIR /app

# install deps
# tesserocr 的安装方式：
#   1. https://pypi.org/project/tesserocr/
#   2. https://bugs.launchpad.net/ubuntu/+source/python3.6/+bug/1768644
RUN deps='ca-certificates python3 cron supervisor tesseract-ocr libtesseract-dev libleptonica-dev dpkg-dev tor libssl-dev'; buildDeps='python3-pip wget vim ipython3 locales'; \
    set -x \
    && apt-get update && apt-get install -y $deps $buildDeps --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

RUN set -x \
    && pip3 install setuptools \
    && pip3 install -U pip

# pip install -r requirements.txt
COPY requirements.txt .
RUN buildDeps='g++ python3-dev'; \
    set -x \
    && apt-get update && apt-get install -y $buildDeps --no-install-recommends \
    && pip3 install -r requirements.txt \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get purge -y --auto-remove $buildDeps

COPY . .

# https://webkul.com/blog/setup-locale-python3/
# Set the locale
RUN locale-gen en_US.UTF-8
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US:en
ENV LC_ALL en_US.UTF-8

RUN ln -s /app/conf/supervisor.conf /etc/supervisor/conf.d/supervisor.conf

CMD ["supervisord", "--nodaemon"]
