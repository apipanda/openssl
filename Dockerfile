FROM tianon/debian:wheezy
MAINTAINER Bernard Ojengwa <bernardojengwa@gmail.com>

RUN echo 'Updating installed packages'
RUN apt-get -y update && apt-get install curl -y

RUN echo 'Setting environment variables'
ENV SECRET_KEY=Bf8pGXxpQ4SAMU+guCFg4t6M1Wd/JLPDSzLVc5hR
ENV PORT=5555


RUN echo 'Install PIP'
RUN curl https://bootstrap.pypa.io/get-pip.py | python $1

RUN echo 'Expose docker port'
EXPOSE 5555