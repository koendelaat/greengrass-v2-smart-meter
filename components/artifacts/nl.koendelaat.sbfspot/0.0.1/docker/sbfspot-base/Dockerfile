FROM ubuntu:20.04

ENV DEBIAN_FRONTEND noninteractive
ENV SBFSPOT_HOME /home/sbfspot
ENV SMADATA /var/smadata
ENV SBFSPOTDIR /opt/sbfspot

ARG user=sbfspot
ARG group=sbfspot
ARG uid=2000
ARG gid=2000

# add our user and group first to make sure their IDs get assigned consistently, regardless of whatever dependencies get added
RUN groupadd -g ${gid} ${group} \
	&& useradd -d "$SBFSPOT_HOME" -u ${uid} -g ${gid} -m -s /bin/bash ${user}

# From version 3.0 no longer uploads to PVoutput.org. This functionality is now in the hands of an upload service (Windows) or daemon (Linux).
# So libcurl3-dev is needed only if you are uploading data to PVoutput.org.
RUN apt-get update \
	&& apt-get install -y --no-install-recommends \
	bluetooth \
	libbluetooth-dev \
	libboost-all-dev \
	sqlite3 \
	libsqlite3-dev \
	libcurl3-dev \
	make \
	g++ \
	cron \
	&& rm -rf /var/lib/apt/lists/*

# Make SBFspot and move installation to SBFSPOTDIR. SBFspot by default installs to /usr/local/bin/sbfspot.3
WORKDIR $SBFSPOT_HOME/sbfspot.3
# wget https://sbfspot.codeplex.com/downloads/get/1575948
ADD dist/SBFspot*.tar.gz $SBFSPOT_HOME/sbfspot.3/

# Compile SBFspot
RUN cd SBFspot && make sqlite && make install_sqlite && cd ..

# Compile SBFspotUploadDaemon
RUN cd SBFspotUploadDaemon && make sqlite && make install_sqlite && cd ..

WORKDIR $SBFSPOT_HOME

RUN mv /usr/local/bin/sbfspot.3 $SBFSPOTDIR \
	&& cp $SBFSPOT_HOME/sbfspot.3/SBFspot/CreateSQLiteDB.sql $SBFSPOTDIR \
	&& rm -rf $SBFSPOT_HOME/sbfspot.3 \
	&& chown -R ${user}:${group} $SBFSPOTDIR

# Setup data directory
RUN mkdir $SMADATA && chown -R ${user}:${group} $SMADATA

RUN touch /var/log/cron.log

VOLUME ["/var/smadata", "/opt/sbfspot"]

USER ${user}

CMD ["/bin/bash"]
