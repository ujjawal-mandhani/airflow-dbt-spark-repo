FROM python:3.10 
RUN apt-get update && apt install telnet nano unixodbc -y
RUN apt --fix-broken install -y && apt install libsasl2-modules-gssapi-mit libsasl2-dev libsasl2-2 lsb-release -y
RUN pip install virtualenv 
RUN curl -sS https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor | tee /etc/apt/trusted.gpg.d/mssql.gpg
RUN curl https://packages.microsoft.com/config/ubuntu/22.04/prod.list > /etc/apt/sources.list.d/mssql-release.list
RUN apt-get update
RUN ACCEPT_EULA=Y apt-get install -y msodbcsql18
RUN apt-get install -y openssh-server
COPY sshd_config /etc/ssh/sshd_config
COPY ssh_config /etc/ssh/ssh_config

WORKDIR /home/
RUN virtualenv dbt_postgres 
RUN /home/dbt_postgres/bin/python -m pip install dbt-core dbt-postgres

WORKDIR /home/
RUN virtualenv dbt_oracle
RUN /home/dbt_oracle/bin/python -m pip install dbt-core dbt-oracle

WORKDIR /home/
RUN virtualenv dbt_spark
RUN /home/dbt_spark/bin/python -m pip install dbt-core dbt-spark[thrift] dbt-spark[PyHive]

WORKDIR /home/
RUN virtualenv dbt_mssql
RUN /home/dbt_mssql/bin/python -m pip install dbt-core dbt-sqlserver

COPY .dbt /root/.dbt/
WORKDIR /home/
# ENTRYPOINT ["tail"]
# CMD ["-f","/dev/null"]
CMD ["sh", "-c", "service ssh start && tail -f /dev/null"]