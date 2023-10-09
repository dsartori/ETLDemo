FROM mcr.microsoft.com/mssql/server:2017-latest-ubuntu

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app
COPY run-initialization.sh ./
COPY entrypoint.sh ./
COPY create-database.sql ./
RUN chmod +x ./run-initialization.sh
RUN chmod +x ./entrypoint.sh

EXPOSE 1433

CMD /bin/bash ./entrypoint.sh