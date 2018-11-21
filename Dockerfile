FROM homdx/kivymd-store:003-36

ARG FUNCRASH_VERSION=0.13
ARG FUNCRASH_HASH=6c122544f281d80057140c51606cccd819ca9dc250d2d3c5d65eb99f691fad08 

COPY . app

RUN sudo chown -Rv user ${WORK_DIR}/app
#USER ${USER}

RUN cd app && patch -p0 <buildozer-docker.patch && echo buildozer android update \
&&  set -ex \
&& wget --quiet https://github.com/homdx/funcrash/releases/download/${FUNCRASH_VERSION}/dot-buildozer.tar.gz \
&& echo "${FUNCRASH_HASH}  dot-buildozer.tar.gz" | sha256sum -c \
&& tar -xf dot-buildozer.tar.gz && rm dot-buildozer.tar.gz \
&& time buildozer android debug || echo "Fix build apk" && cp -vf /home/user/hostcwd/app/.buildozer/android/platform/build/dists/funcrash/bin/FunCrash*.apk ~/

CMD tail -f /var/log/faillog

#ENTRYPOINT ["buildozer"]
