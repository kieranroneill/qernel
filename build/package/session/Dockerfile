FROM redis:7-alpine

# setup os
RUN apk add --no-cache gettext

# copy configuratuion files
COPY ./build/package/session/redis.conf /usr/local/etc/redis/redis.conf
COPY ./build/package/session/users.acl.template /usr/local/etc/redis/users.acl.template
COPY ./build/package/session/entrypoint.sh /usr/local/bin/entrypoint.sh

RUN chmod +x /usr/local/bin/entrypoint.sh

ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]

CMD ["redis-server", "/usr/local/etc/redis/redis.conf"]
