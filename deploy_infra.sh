#!/bin/bash

export HADOOP_VERSION="3.3.6"
export SPARK_VERSION="3.5.0"
export SCALA_VERSION="2.12"
export JAVA_VERSION="11"
export SPARK_LOCAL_IP=192.168.1.128


create_directories() {
    echo "Création des répertoires..."
    mkdir -p ~/data_lake/{raw,bronze,silver,gold}
    mkdir -p ~/data_lake/raw/{transactions,web_logs,social_media,advertising}
    mkdir -p ~/hadoop_tmp
    mkdir -p ~/spark_tmp
}

install_dependencies() {
    echo "Installation des dépendances..."
    sudo apt-get update
    sudo apt-get install -y openjdk-${JAVA_VERSION}-jdk wget ssh pdsh
}

install_hadoop() {
    echo "Installation de Hadoop..."
    cd ~
    wget https://downloads.apache.org/hadoop/common/hadoop-${HADOOP_VERSION}/hadoop-${HADOOP_VERSION}.tar.gz
    tar -xzf hadoop-${HADOOP_VERSION}.tar.gz
    mv hadoop-${HADOOP_VERSION} hadoop
    rm hadoop-${HADOOP_VERSION}.tar.gz

    echo "Configuration des variables d'environnement Hadoop..."
    cat >> ~/.bashrc << 'EOF'
export HADOOP_HOME=~/hadoop
export HADOOP_INSTALL=$HADOOP_HOME
export HADOOP_MAPRED_HOME=$HADOOP_HOME
export HADOOP_COMMON_HOME=$HADOOP_HOME
export HADOOP_HDFS_HOME=$HADOOP_HOME
export YARN_HOME=$HADOOP_HOME
export HADOOP_COMMON_LIB_NATIVE_DIR=$HADOOP_HOME/lib/native
export PATH=$PATH:$HADOOP_HOME/sbin:$HADOOP_HOME/bin
EOF
    source ~/.bashrc
}

configure_hadoop() {
    echo "Configuration des fichiers Hadoop..."
    
    # core-site.xml
    cat > ~/hadoop/etc/hadoop/core-site.xml << 'EOF'
<?xml version="1.0" encoding="UTF-8"?>
<?xml-stylesheet type="text/xsl" href="configuration.xsl"?>
<configuration>
    <property>
        <name>fs.defaultFS</name>
        <value>hdfs://localhost:9000</value>
    </property>
    <property>
        <name>hadoop.tmp.dir</name>
        <value>/home/${USER}/hadoop_tmp</value>
    </property>
</configuration>
EOF

    # hdfs-site.xml
    cat > ~/hadoop/etc/hadoop/hdfs-site.xml << 'EOF'
<?xml version="1.0" encoding="UTF-8"?>
<?xml-stylesheet type="text/xsl" href="configuration.xsl"?>
<configuration>
    <property>
        <name>dfs.replication</name>
        <value>1</value>
    </property>
    <property>
        <name>dfs.namenode.name.dir</name>
        <value>/home/${USER}/hadoop_tmp/namenode</value>
    </property>
    <property>
        <name>dfs.datanode.data.dir</name>
        <value>/home/${USER}/hadoop_tmp/datanode</value>
    </property>
</configuration>
EOF

    # mapred-site.xml
    cat > ~/hadoop/etc/hadoop/mapred-site.xml << 'EOF'
<?xml version="1.0" encoding="UTF-8"?>
<?xml-stylesheet type="text/xsl" href="configuration.xsl"?>
<configuration>
    <property>
        <name>mapreduce.framework.name</name>
        <value>yarn</value>
    </property>
</configuration>
EOF

    # yarn-site.xml
    cat > ~/hadoop/etc/hadoop/yarn-site.xml << 'EOF'
<?xml version="1.0" encoding="UTF-8"?>
<?xml-stylesheet type="text/xsl" href="configuration.xsl"?>
<configuration>
    <property>
        <name>yarn.nodemanager.aux-services</name>
        <value>mapreduce_shuffle</value>
    </property>
    <property>
        <name>yarn.nodemanager.env-whitelist</name>
        <value>JAVA_HOME,HADOOP_COMMON_HOME,HADOOP_HDFS_HOME,HADOOP_CONF_DIR,CLASSPATH_PREPEND_DISTCACHE,HADOOP_YARN_HOME,HADOOP_HOME,PATH,LANG,TZ,HADOOP_MAPRED_HOME</value>
    </property>
</configuration>
EOF
}

install_spark() {
    echo "Installation de Spark..."
    cd ~
    wget https://downloads.apache.org/spark/spark-${SPARK_VERSION}/spark-${SPARK_VERSION}-bin-hadoop3.tgz
    tar -xzf spark-${SPARK_VERSION}-bin-hadoop3.tgz
    mv spark-${SPARK_VERSION}-bin-hadoop3 spark
    rm spark-${SPARK_VERSION}-bin-hadoop3.tgz

    echo "Configuration des variables d'environnement Spark..."
    cat >> ~/.bashrc << 'EOF'
export SPARK_HOME=~/spark
export PATH=$PATH:$SPARK_HOME/bin
export PYSPARK_PYTHON=python3
EOF
    source ~/.bashrc

    cp $SPARK_HOME/conf/spark-env.sh.template $SPARK_HOME/conf/spark-env.sh
    echo "export JAVA_HOME=/usr/lib/jvm/java-${JAVA_VERSION}-openjdk-amd64" >> $SPARK_HOME/conf/spark-env.sh
    echo "export HADOOP_HOME=~/hadoop" >> $SPARK_HOME/conf/spark-env.sh
    echo "export SPARK_LOCAL_IP=localhost" >> $SPARK_HOME/conf/spark-env.sh

    cp $SPARK_HOME/conf/spark-defaults.conf.template $SPARK_HOME/conf/spark-defaults.conf
    echo "spark.master                     yarn" >> $SPARK_HOME/conf/spark-defaults.conf
    echo "spark.driver.memory              512m" >> $SPARK_HOME/conf/spark-defaults.conf
    echo "spark.yarn.am.memory             512m" >> $SPARK_HOME/conf/spark-defaults.conf
    echo "spark.executor.memory            512m" >> $SPARK_HOME/conf/spark-defaults.conf
}

configure_ssh() {
    echo "Configuration de SSH..."
    ssh-keygen -t rsa -P '' -f ~/.ssh/id_rsa
    cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys
    chmod 0600 ~/.ssh/authorized_keys
}

init_hdfs() {
    echo "Initialisation de HDFS..."
    hdfs namenode -format

    start-dfs.sh
    hdfs dfs -mkdir -p /data_lake/{raw,bronze,silver,gold}
    hdfs dfs -mkdir -p /data_lake/raw/{transactions,web_logs,social_media,advertising}
    stop-dfs.sh
}

main() {
    create_directories
    install_dependencies
    configure_ssh
    install_hadoop
    configure_hadoop
    install_spark
    init_hdfs
    
    echo "Installation terminée !"
    echo "Pour démarrer les services :"
    echo "1. start-dfs.sh"
    echo "2. start-yarn.sh"
}

main