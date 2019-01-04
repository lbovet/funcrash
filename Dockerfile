FROM homdx/kivymd-store:003-36

ARG FUNCRASH_VERSION=0.17
ARG FUNCRASH_HASH=e9e9c3d8a66a770ea3dd101fefc342c24a7e3e37133cbb8c296901bff284c7da

COPY . app

RUN sudo chown -Rv user ${WORK_DIR}/app
#USER ${USER}

RUN cd app && patch -p0 <buildozer-docker.patch && patch -p0 <main-without-cred.patch && echo buildozer android update \
&&  set -ex \
&& wget --quiet https://github.com/homdx/funcrash/releases/download/${FUNCRASH_VERSION}/dot-buildozer.tar.gz \
&& echo "${FUNCRASH_HASH}  dot-buildozer.tar.gz" | sha256sum -c \
&& tar -xf dot-buildozer.tar.gz && rm dot-buildozer.tar.gz \
&& time buildozer android debug || echo "Fix build apk" && cp -vf /home/user/hostcwd/app/.buildozer/android/platform/build/dists/funcrash/bin/FunCrash*.apk ~/

CMD tail -f /var/log/faillog

#ENTRYPOINT ["buildozer"]
