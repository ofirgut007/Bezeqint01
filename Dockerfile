FROM centos:7
MAINTAINER Ofir Gutmacher
RUN yum install -y python
COPY production.py production.py
RUN python production.py