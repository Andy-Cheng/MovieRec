# Use nvidia/cuda image
FROM pytorch/pytorch:1.11.0-cuda11.3-cudnn8-devel

# set bash as current shell
RUN chsh -s /bin/bash
SHELL ["/bin/bash", "-c"]

# # install anaconda
# RUN apt-get update
# RUN apt-get install -y wget bzip2 ca-certificates libglib2.0-0 libxext6 libsm6 libxrender1 git mercurial subversion && \
#         apt-get clean
# RUN wget --quiet https://repo.anaconda.com/archive/Anaconda3-2020.02-Linux-x86_64.sh -O ~/anaconda.sh && \
#         /bin/bash ~/anaconda.sh -b -p /opt/conda && \
#         rm ~/anaconda.sh && \
#         ln -s /opt/conda/etc/profile.d/conda.sh /etc/profile.d/conda.sh && \
#         echo ". /opt/conda/etc/profile.d/conda.sh" >> ~/.bashrc && \
#         find /opt/conda/ -follow -type f -name '*.a' -delete && \
#         find /opt/conda/ -follow -type f -name '*.js.map' -delete && \
#         /opt/conda/bin/conda clean -afy


# ARG PYTHON_VERSION=3.8

# RUN apt-get update
# RUN apt-get install -y wget bzip2 ca-certificates libglib2.0-0 libxext6 libsm6 libxrender1 git mercurial subversion curl && \
#         apt-get clean


# RUN curl -fsSL -v -o ~/miniconda.sh -O  https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh  && \
#     chmod +x ~/miniconda.sh && \
#     /bin/bash ~/miniconda.sh -b -p /opt/conda && \
#     rm ~/miniconda.sh && \
#     ln -s /opt/conda/etc/profile.d/conda.sh /etc/profile.d/conda.sh && \
#     echo ". /opt/conda/etc/profile.d/conda.sh" >> ~/.bashrc && \
#     find /opt/conda/ -follow -type f -name '*.a' -delete && \
#     find /opt/conda/ -follow -type f -name '*.js.map' -delete && \
#     /opt/conda/bin/conda install -y python=${PYTHON_VERSION} && \
#     /opt/conda/bin/conda clean -afy

# # set path to conda
# ENV PATH /opt/conda/bin:$PATH

# install python
# RUN apt-get -y update \
#     && apt-get install -y software-properties-common \
#     && apt-get -y update \
#     && add-apt-repository universe
# RUN apt-get -y update
# RUN apt-get -y install git
# RUN apt-get -y install python3.8
# RUN apt-get -y install python3-pip
# RUN ln /usr/bin/python3.7 /usr/bin/python \ 
#     && ln /usr/bin/pip3 /usr/bin/pip