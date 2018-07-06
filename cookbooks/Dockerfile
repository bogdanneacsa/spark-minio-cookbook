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
    tar -xvf hadoop-2.8.3.tar.gz hadoop-2.8.3/lib/native && \
    ln -s hadoop-2.8.3 hadoop && \
    echo Hadoop 2.8.3 native libraries installed in /opt/hadoop/lib/native
RUN ls -R /opt/hadoop/

RUN mkdir -p /opt && \
    cd /opt && \
    curl http://www.eu.apache.org/dist/spark/spark-2.3.0/spark-2.3.0-bin-without-hadoop.tgz -o spark-2.3.0-bin-without-hadoop.tgz && \
    tar -xvf spark-2.3.0-bin-without-hadoop.tgz && \
    ln -s spark-2.3.0-bin-without-hadoop spark && \
    echo Spark 2.3.0 installed in /opt

RUN curl http://central.maven.org/maven2/org/apache/hadoop/hadoop-aws/2.8.2/hadoop-aws-2.8.2.jar -o /opt/spark/jars/hadoop-aws-2.8.2.jar
RUN curl http://central.maven.org/maven2/org/apache/httpcomponents/httpclient/4.5.3/httpclient-4.5.3.jar -o httpclient-4.5.3.jar
RUN curl http://central.maven.org/maven2/joda-time/joda-time/2.9.9/joda-time-2.9.9.jar -o joda-time-2.9.9.jar
RUN curl http://central.maven.org/maven2/com/amazonaws/aws-java-sdk-core/1.11.234/aws-java-sdk-core-1.11.234.jar -o aws-java-sdk-core-1.11.234
RUN curl http://central.maven.org/maven2/com/amazonaws/aws-java-sdk/1.11.234/aws-java-sdk-1.11.234.jar -o aws-java-sdk-1.11.234.jar
RUN curl http://central.maven.org/maven2/com/amazonaws/aws-java-sdk-kms/1.11.234/aws-java-sdk-kms-1.11.234.jar -o aws-java-sdk-kms-1.11.234.jar
RUN curl http://central.maven.org/maven2/com/amazonaws/aws-java-sdk-s3/1.11.234/aws-java-sdk-s3-1.11.234.jar -o aws-java-sdk-s3-1.11.234.jar

RUN pip3 install pyspark

ADD minio_connection.py /opt
ENV PATH $PATH:/opt/spark/bin
ENTRYPOINT ["spark-submit", "/opt/minio_connection.py"]