# Run QGIS in Docker

## Install docker

for centos or aws linux
```bash
sudo yum install docker
```

for ubuntu
```bash
sudo apt-get install docker.io
```

add user to docker group (optional), to run docker without sudo

```bash
sudo usermod -a -G docker ec2-user
id ec2-user
newgrp docker
sudo systemctl enable docker.service
sudo systemctl start docker.service
```

## Build docker image and run

in the folder that contains `Dockerfile`

```bash
docker build -t qgis .
```

after build, run the image with `-it` option, to enter the container

```bash
docker run -it qgis
```
with `-v` option, to mount folder
```bash
docker run -it -v ./AutoRun:/AutoRun qgis
```

in the container, run export_image.py
```bash
python3 ./rosa_export_image/main.py -i AutoRun/D20220918/E1444 -o images
```

copy images to host
*(containerId can be found by `docker ps`)*
```bash
docker cp <containerId>:/images ./images
```


---

## legacy

```bash
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
su
bash Miniconda3-latest-Linux-x86_64.sh -bfp /miniconda
/miniconda/condabin/conda update -n base -c defaults conda
/miniconda/condabin/conda init bash
```

```bash
conda config --set auto_activate_base false
conda create --name qgis_env
conda activate qgis_env
conda install qgis matplotlib numpy -c conda-forge
```

```bash
yum install mesa-libGL Xvfb
```

```bash
cp msjh.ttc /miniconda/envs/qgis_env/lib/fonts/
fc-cache -f -v
```

```python
import matplotlib.font_manager
matplotlib.font_manager._load_fontmanager(try_read_cache=False)
```

```bash
conda activate qgis_env
Xvfb :99 -ac -noreset & 
export DISPLAY=:99
python export_image.py -i AutoRun/D20220918/E1444
```
