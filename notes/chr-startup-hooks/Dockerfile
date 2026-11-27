FROM mikrotik/chr:7.26beta7@sha256:b68f34a50544f6464d592cdd07ecc1d08017d6ec6837ac42b7dbe701d3c1ca6a
RUN apk add --no-cache iproute2-tc && mkdir -p /etc/chr/start.d
COPY --chmod=755 start.sh /start.sh
