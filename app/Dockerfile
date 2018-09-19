FROM ubuntu:18.04
MAINTAINER Rollin Thomas <rcthomas@lbl.gov>

ENV DEBIAN_FRONTEND noninteractive
ENV LANG C.UTF-8

RUN \
    apt-get update          &&  \
    apt-get --yes upgrade   &&  \
    apt-get --yes install       \
        bzip2                   \
        curl                    \
        vim

RUN \
    curl -o /tmp/miniconda3.sh https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh    &&  \
    /bin/bash /tmp/miniconda3.sh -b -p /opt/anaconda3   &&  \
    rm -rf /tmp/miniconda3

ENV PATH=/opt/anaconda3/bin:$PATH

RUN \
    conda update --yes conda    &&  \
    conda install --yes             \
        flask                       \
        gunicorn                    \
        pymongo

ADD app.py docker-entrypoint.sh /srv/
ADD templates /srv/templates/

WORKDIR /srv
RUN chmod +x docker-entrypoint.sh
CMD ["gunicorn", "app:app", "--name", "app", "-b", ":8000", "--log-level=debug", "--log-file=-"]
ENTRYPOINT ["./docker-entrypoint.sh"]
