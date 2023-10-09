# [Choice] Python version: 3, 3.8, 3.7, 3.6
ARG VARIANT=3
FROM mcr.microsoft.com/vscode/devcontainers/python:0-${VARIANT}

ENV PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100 \
  POETRY_VERSION=1.2.2

# Update args in docker-compose.yaml to set the UID/GID of the "vscode" user.
ARG USER_UID=1000
ARG USER_GID=$USER_UID
RUN if [ "$USER_GID" != "1000" ] || [ "$USER_UID" != "1000" ]; then groupmod --gid $USER_GID vscode && usermod --uid $USER_UID --gid $USER_GID vscode; fi

# [Choice] Node.js version: none, lts/*, 16, 14, 12, 10
ARG NODE_VERSION="none"
RUN if [ "${NODE_VERSION}" != "none" ]; then su vscode -c "umask 0002 && . /usr/local/share/nvm/nvm.sh && nvm install ${NODE_VERSION} 2>&1"; fi

RUN apt-get update \
    && apt-get install --no-install-recommends -y \
        curl \
        build-essential

RUN pip install "poetry==$POETRY_VERSION"

ENV PATH=$HOME/.poetry/bin:$PATH

# unixodbc needs to be installed before adding microsoft repo
# and installing mssql-tools
# Note: Order matters! Layer will fail to build otherwise
RUN export DEBIAN_FRONTEND=noninteractive \
    && apt-get update \
    && apt-get install -y --no-install-recommends software-properties-common unixodbc unixodbc-dev \
    && curl -sSL https://packages.microsoft.com/keys/microsoft.asc | sudo apt-key add - \
    && apt-add-repository https://packages.microsoft.com/debian/11/prod \
    && curl https://packages.microsoft.com/config/debian/10/prod.list > /etc/apt/sources.list.d/mssql-release.list \
    && apt-get update \
    && ACCEPT_EULA=Y apt-get install -y msodbcsql17 mssql-tools libgssapi-krb5-2 \
    && apt-get clean

ENV PATH="$PATH:/opt/mssql-tools/bin"