FROM koendelaat/sbfspot-base:0.0.3

ENV SMADATA /var/smadata
ENV SBFSPOTDIR /opt/sbfspot

ARG user=sbfspot

VOLUME ["/var/smadata", "/opt/sbfspot"]

USER root

COPY --chown=2000:2000 SBFspot.sh $SBFSPOTDIR/SBFspot.sh

ADD crontab /etc/cron.d/sbfspot-collector

RUN chmod 0644 /etc/cron.d/sbfspot-collector
RUN crontab /etc/cron.d/sbfspot-collector

CMD cron && tail -f /var/log/cron.log

