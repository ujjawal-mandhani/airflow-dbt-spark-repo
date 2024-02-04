FROM openjdk:8
ENV SPARK_VERSION 3.3.1
ENV SPARK_HOME /usr/local/share/spark
RUN curl -fL "https://archive.apache.org/dist/spark/spark-$SPARK_VERSION/spark-$SPARK_VERSION-bin-hadoop3.tgz" | tar xfz - -C /usr/local/share && \
    mv "/usr/local/share/spark-$SPARK_VERSION-bin-hadoop3" "$SPARK_HOME"
ENV PATH "$PATH:$SPARK_HOME/bin"
RUN apt-get update && apt-get install -y openssh-server
COPY sshd_config /etc/ssh/sshd_config
COPY ssh_config /etc/ssh/ssh_config
COPY spark-env.sh /usr/local/share/spark/conf/spark-env.sh
COPY slaves /usr/local/share/spark/conf/slaves
CMD ["sh", "-c", "service ssh start && sh -c /usr/local/share/spark/sbin/start-master.sh && sh -c /usr/local/share/spark/sbin/start-thriftserver.sh && sh -c /usr/local/share/spark/sbin/start-all.sh && tail -f /dev/null"]