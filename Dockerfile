FROM debian:11.1-slim

ENV DISPLAY=:1 \
    VNC_PORT=5901 \
    NO_VNC_PORT=6901 \
    VNC_COL_DEPTH=32 \
    VNC_RESOLUTION=1920x1080

# No interactive frontend during docker build
ENV DEBIAN_FRONTEND=noninteractive


RUN apt-get update && \
    apt-get install --no-install-recommends -y \
    xvfb xauth dbus-x11 xfce4 xfce4-terminal \
    wget sudo curl gpg git bzip2 vim procps python x11-xserver-utils \
    libnss3 libnspr4 libasound2 libgbm1 ca-certificates fonts-liberation xdg-utils \
    tigervnc-standalone-server tigervnc-common firefox-esr; \
    curl http://ftp.us.debian.org/debian/pool/main/liba/libappindicator/libappindicator3-1_0.4.92-7_amd64.deb --output /opt/libappindicator3-1_0.4.92-7_amd64.deb && \
    curl http://ftp.us.debian.org/debian/pool/main/libi/libindicator/libindicator3-7_0.5.0-4_amd64.deb --output /opt/libindicator3-7_0.5.0-4_amd64.deb && \
    apt-get install -y /opt/libappindicator3-1_0.4.92-7_amd64.deb /opt/libindicator3-7_0.5.0-4_amd64.deb; \
    rm -vf /opt/lib*.deb; \
    apt-get clean; \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*


RUN apt-get update
RUN apt-get -y install wget unzip nano python3-pip git libu2f-udev
#RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
#RUN dpkg -i google-chrome-stable_current_amd64.deb
RUN python3 -m pip install selenium
RUN pip install webdriver-manager
#RUN wget https://storage.googleapis.com/chrome-for-testing-public/126.0.6478.126/linux64/chromedriver-linux64.zip
#RUN unzip chromedriver-linux64.zip
#RUN mv ./chromedriver-linux64/chromedriver /usr/bin/
RUN wget https://github.com/mozilla/geckodriver/releases/download/v0.34.0/geckodriver-v0.34.0-linux64.tar.gz
RUN tar -xvzf geckodriver*
RUN chmod +x geckodriver
RUN mv geckodriver /usr/local/bin/ 

COPY main.py /home/dockeruser/Desktop/main.py
RUN chmod 777 /home/dockeruser/Desktop/main.py



ENV TERM xterm
# Install NOVNC.
RUN     git clone --branch v1.2.0 --single-branch https://github.com/novnc/noVNC.git /opt/noVNC; \
        git clone --branch v0.9.0 --single-branch https://github.com/novnc/websockify.git /opt/noVNC/utils/websockify; \
        ln -s /opt/noVNC/vnc.html /opt/noVNC/index.html

# disable shared memory X11 affecting Chromium
ENV QT_X11_NO_MITSHM=1 \
    _X11_NO_MITSHM=1 \
    _MITSHM=0


# give every user read write access to the "/root" folder where the binary is cached
RUN ls -la /root
RUN chmod 777 /root && mkdir /src

RUN groupadd -g 61000 dockeruser; \
    useradd -g 61000 -l -m -s /bin/bash -u 61000 dockeruser

COPY assets/config/ /home/dockeruser/.config

RUN mkdir /home/dockeruser/.config/autostart
COPY autostartpython.desktop /home/dockeruser/.config/autostart/autostartpython.desktop
RUN chmod 777 /home/dockeruser/.config/autostart/autostartpython.desktop

RUN chown -R dockeruser:dockeruser /home/dockeruser;\
    chmod -R 777 /home/dockeruser ;\
    adduser dockeruser sudo;\
    echo '%sudo ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers

USER dockeruser
# versions of local tools
RUN echo  "debian version:  $(cat /etc/debian_version) \n" \
          "user:            $(whoami) \n"

COPY scripts/entrypoint.sh /src

#Expose port 5901 to view display using VNC Viewer
EXPOSE 5901 6901
ENTRYPOINT ["/src/entrypoint.sh"]