FROM koendelaat/sbfspot-base:0.0.6

ENV SMADATA /var/smadata
ENV SBFSPOTDIR /opt/sbfspot

ARG user=sbfspot

VOLUME ["/var/smadata", "/opt/sbfspot"]

COPY --chown=2000:2000 SBFspotUploadDaemon.sh $SBFSPOTDIR/SBFspotUploadDaemon.sh

USER ${user}

CMD bash -C '/opt/sbfspot/SBFspotUploadDaemon.sh';'bash'
