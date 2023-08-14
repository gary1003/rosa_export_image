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
yum install mesa-libGL
```

```bash
cp msjh.ttc /miniconda/envs/qgis_env/lib/fonts/
fc-cache -f -v
```

```python
import matplotlib
matplotlib.font_manager._rebuild()
```

```bash
conda activate qgis_env
python export_image.py -i AutoRun/D20220918/E1444
```