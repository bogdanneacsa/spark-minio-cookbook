FROM jopgen/t-base:v2

RUN yum install -y https://centos7.iuscommunity.org/ius-release.rpm \
    && yum install -y python36u \
    && yum install -y python36u-pip \
    && yum install -y python36u-devel \
    && yum install -y openldap-devel \
    && yum install -y gcc-c++

RUN mkdir -p /opt && \
    cd /opt && \
    curl http://archive.apache.org/dist/hadoop/common/hadoop-2.8.3/hadoop-2.8.3.tar.gz -o hadoop-2.8.3.tar.gz && \
    tar -xvf hadoop-2.8.3.tar.gz && \
    ln -s hadoop-2.8.3 hadoop && \
    echo Hadoop 2.8.3 native libraries installed in /opt/hadoop/lib/native
RUN ls -R /opt/hadoop/

RUN mkdir -p /opt && \
    cd /opt && \
    curl http://ftp.heanet.ie/mirrors/www.apache.org/dist/spark/spark-2.3.0/spark-2.3.0-bin-without-hadoop.tgz -o spark-2.3.0-bin-without-hadoop.tgz && \
    tar -xvf spark-2.3.0-bin-without-hadoop.tgz && \
    ln -s spark-2.3.0-bin-without-hadoop spark && \
    echo Spark 2.3.0 installed in /opt

RUN curl http://central.maven.org/maven2/org/apache/hadoop/hadoop-aws/2.8.2/hadoop-aws-2.8.2.jar -o /opt/spark-2.3.0-bin-without-hadoop/bin/hadoop-aws-2.8.2.jar
RUN curl http://central.maven.org/maven2/org/apache/httpcomponents/httpclient/4.5.3/httpclient-4.5.3.jar -o /opt/spark-2.3.0-bin-without-hadoop/bin/httpclient-4.5.3.jar
RUN curl http://central.maven.org/maven2/joda-time/joda-time/2.9.9/joda-time-2.9.9.jar -o /opt/spark-2.3.0-bin-without-hadoop/bin/joda-time-2.9.9.jar
RUN curl http://central.maven.org/maven2/com/amazonaws/aws-java-sdk-core/1.11.234/aws-java-sdk-core-1.11.234.jar -o /opt/spark-2.3.0-bin-without-hadoop/bin/aws-java-sdk-core-1.11.234.jar
RUN curl http://central.maven.org/maven2/com/amazonaws/aws-java-sdk/1.11.234/aws-java-sdk-1.11.234.jar -o /opt/spark-2.3.0-bin-without-hadoop/bin/aws-java-sdk-1.11.234.jar
RUN curl http://central.maven.org/maven2/com/amazonaws/aws-java-sdk-kms/1.11.234/aws-java-sdk-kms-1.11.234.jar -o /opt/spark-2.3.0-bin-without-hadoop/bin/aws-java-sdk-kms-1.11.234.jar
RUN curl http://central.maven.org/maven2/com/amazonaws/aws-java-sdk-s3/1.11.234/aws-java-sdk-s3-1.11.234.jar -o /opt/spark-2.3.0-bin-without-hadoop/bin/aws-java-sdk-s3-1.11.234.jar

RUN pip install pyspark
RUN pip install pytz

# JAVA
ARG JAVA_MAJOR_VERSION=8
ARG JAVA_UPDATE_VERSION=131
ARG JAVA_BUILD_NUMBER=11
ENV JAVA_HOME /usr/jdk1.${JAVA_MAJOR_VERSION}.0_${JAVA_UPDATE_VERSION}

ENV PATH $PATH:$JAVA_HOME/bin
RUN curl -sL --retry 3 --insecure \
  --header "Cookie: oraclelicense=accept-securebackup-cookie;" \
  "http://download.oracle.com/otn-pub/java/jdk/${JAVA_MAJOR_VERSION}u${JAVA_UPDATE_VERSION}-b${JAVA_BUILD_NUMBER}/d54c1d3a095b4ff2b6607d096fa80163/server-jre-${JAVA_MAJOR_VERSION}u${JAVA_UPDATE_VERSION}-linux-x64.tar.gz" \
  | gunzip \
  | tar x -C /usr/ \
  && ln -s $JAVA_HOME /usr/java \
  && rm -rf $JAVA_HOME/man

ENV HADOOP_HOME /opt/hadoop-2.8.3
ENV PATH $PATH:$HADOOP_HOME/bin
#ENV SPARK_DIST_CLASSPATH $(hadoop classpath)
ENV SPARK_CLASSPATH /opt/spark-2.3.0-bin-without-hadoop/bin:$SPARK_DIST_CLASSPATH

ENV HADOOP_CONF_DIR=$HADOOP_HOME/etc/hadoop
#ENV PATH $PATH:$HADOOP_HOME/bin

ENV SPARK_HOME /opt/spark-2.3.0-bin-without-hadoop
ENV SPARK_DIST_CLASSPATH "$HADOOP_HOME/etc/hadoop/*:$HADOOP_HOME/share/hadoop/common/lib/*:$HADOOP_HOME/share/hadoop/common/*:$HADOOP_HOME/share/hadoop/hdfs/*:$HADOOP_HOME/share/hadoop/hdfs/lib/*:$HADOOP_HOME/share/hadoop/hdfs/*:$HADOOP_HOME/share/hadoop/yarn/lib/*:$HADOOP_HOME/share/hadoop/yarn/*:$HADOOP_HOME/share/hadoop/mapreduce/lib/*:$HADOOP_HOME/share/hadoop/mapreduce/*:$HADOOP_HOME/share/hadoop/tools/lib/*"
ENV SPARK_DIST_CLASSPATH /opt/spark-2.3.0-bin-without-hadoop/bin:$SPARK_DIST_CLASSPATH
ENV SPARK_CLASSPATH $SPARK_HOME/bin:$SPARK_DIST_CLASSPATH
#ENV PATH $PATH:${SPARK_HOME}/bin

RUN cp /opt/spark-2.3.0-bin-without-hadoop/bin/hadoop-aws-2.8.2.jar /opt/hadoop-2.8.3/share/hadoop/common/lib
RUN cp /opt/spark-2.3.0-bin-without-hadoop/bin/httpclient-4.5.3.jar /opt/hadoop-2.8.3/share/hadoop/common/lib
RUN cp /opt/spark-2.3.0-bin-without-hadoop/bin/joda-time-2.9.9.jar /opt/hadoop-2.8.3/share/hadoop/common/lib
RUN cp /opt/spark-2.3.0-bin-without-hadoop/bin/aws-java-sdk-core-1.11.234.jar /opt/hadoop-2.8.3/share/hadoop/common/lib
RUN cp /opt/spark-2.3.0-bin-without-hadoop/bin/aws-java-sdk-1.11.234.jar /opt/hadoop-2.8.3/share/hadoop/common/lib
RUN cp /opt/spark-2.3.0-bin-without-hadoop/bin/aws-java-sdk-kms-1.11.234.jar /opt/hadoop-2.8.3/share/hadoop/common/lib
RUN cp /opt/spark-2.3.0-bin-without-hadoop/bin/aws-java-sdk-s3-1.11.234.jar /opt/hadoop-2.8.3/share/hadoop/common/lib

RUN rm -r /usr/lib/python2.7/site-packages/pyspark/jars

COPY minio_connection.py /opt
#ENTRYPOINT ["ls"]
CMD ["spark-submit", "/opt/minio_connection.py"]