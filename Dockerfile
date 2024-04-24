FROM apache/airflow
RUN pip install psycopg2-binary apache-airflow-providers-apache-spark apache-airflow-providers-oracle apache-airflow-providers-smtp apache-airflow-providers-amazon pandas
USER root 
RUN apt-get update -y && apt install default-jre default-jdk openssh-server -y
ENV SPARK_VERSION 3.3.1
ENV SPARK_HOME /usr/local/share/spark
RUN curl -fL "https://archive.apache.org/dist/spark/spark-$SPARK_VERSION/spark-$SPARK_VERSION-bin-hadoop3.tgz" | tar xfz - -C /usr/local/share && \
    mv "/usr/local/share/spark-$SPARK_VERSION-bin-hadoop3" "$SPARK_HOME"
ENV PATH "$PATH:$SPARK_HOME/bin"
COPY ./spark-cluster/sshd_config /etc/ssh/sshd_config
COPY ./spark-cluster/ssh_config /etc/ssh/ssh_config
USER airflow
RUN mkdir -p /opt/airflow/spark_scripts
COPY ./spark-cluster/spark-jobs/spark_job.py /opt/airflow/spark_scripts/
ENTRYPOINT [ "bash", "-c", "/entrypoint airflow db init && (/entrypoint airflow webserver & /entrypoint airflow scheduler)" ]
CMD []