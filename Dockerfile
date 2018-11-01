FROM homdx/kivymd-store:001


RUN mkdir app

COPY . app

#USER root
#RUN chown user /home/user/ -R && chown -R user /home/user/hostcwd
#USER ${USER}

RUN cd app && time buildozer android debug || echo "Fix build apk" && cp -vf /home/user/hostcwd/app/.buildozer/android/platform/build/dists/funcrash/bin/FunCrash*.apk ~/

CMD tail -f /var/log/faillog

#ENTRYPOINT ["buildozer"]
