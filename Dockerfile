FROM opengisch/qgis:ltr-jammy

ENV QGIS_PREFIX_PATH=/usr
ENV QT_QPA_PLATFORM=offscreen
ENV XDG_RUNTIME_DIR=/tmp/runtime-root
ENV PATH="/bin:${PATH}"
ENV PYTHONPATH="/bin/python3:${PYTHONPATH}"

# copy all files to the container
COPY . /rosa_export_image

RUN apt-get update && apt-get install -y python3-pip
# RUN cp msjh.ttc /usr/share/fonts
COPY msjh.ttc /usr/share/fonts
RUN fc-cache -f -v

RUN python3 -m pip install --upgrade pip
RUN python3 -m pip install --no-cache-dir matplotlib numpy

CMD ["/bin/bash"]