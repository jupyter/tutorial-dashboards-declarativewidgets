FROM jupyter/pyspark-notebook:1d374670daaa

# Become root to do the apt-gets
USER root

RUN apt-get update && \
		apt-get install -y curl && \
		curl --silent --location https://deb.nodesource.com/setup_0.12 | sudo bash - && \
		apt-get install --yes nodejs && \
		npm install -g bower

# Do the pip installs as the unprivileged notebook user
USER jovyan

# Install dashboard layout and preview within Jupyter Notebook
ARG DASHBOARDS_VER
RUN pip install "jupyter_dashboards==$DASHBOARDS_VER" && \
	jupyter dashboards quick-setup --sys-prefix

# Install declarative widgets for Jupyter Notebook
ARG DECLWIDGETS_VER
RUN pip install "jupyter_declarativewidgets==$DECLWIDGETS_VER" && \
	jupyter declarativewidgets quick-setup --sys-prefix

# Install content management to support dashboard bundler options
ARG CMS_VER
ARG BUNDLER_VER
RUN pip install "jupyter_cms==$CMS_VER" && \
	jupyter cms quick-setup --sys-prefix
RUN pip install "jupyter_dashboards_bundlers==$BUNDLER_VER" && \
	jupyter dashboards_bundlers quick-setup --sys-prefix

RUN pip install softlayer
RUN pip install git+https://github.com/parente/dizzybot
