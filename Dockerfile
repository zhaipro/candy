# http://container-solutions.com/6-dockerfile-tips-official-images/
FROM ubuntu:16.04
MAINTAINER 'unkonwn' unkonwn@unkonwn.com
WORKDIR /app

# install deps
# 阿里源[无奈脸]
COPY conf/sources.list /etc/apt/sources.list
RUN deps='ca-certificates python3 cron supervisor tesseract-ocr libtesseract-dev libleptonica-dev tor'; buildDeps='python3-pip wget vim ipython3'; \
    set -x \
    && apt-get update && apt-get install -y $deps $buildDeps --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

# 豆瓣源
COPY conf/pip.conf /root/.pip/pip.conf
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

RUN crontab conf/crontab
RUN ln -s /app/conf/supervisor.conf /etc/supervisor/conf.d/supervisor.conf

RUN chmod u+x ./run.sh
CMD ["./run.sh"]
