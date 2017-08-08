FROM centos:7
MAINTAINER Ofir Gutmacher
RUN yum install -y python
COPY main.py main.py
RUN python main.py