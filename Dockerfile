FROM python:3
USER root

RUN apt-get update

ENV LANG ja_JP.UTF-8
ENV LANGUAGE ja_JP:ja
ENV LC_ALL ja_JP.UTF-8
ENV TZ JST-9
ENV TERM xter
EXPOSE 80

WORKDIR /code
COPY /src /code

RUN apt-get install -y vim less
RUN pip install --upgrade pip
RUN pip install --upgrade setuptools
RUN pip install pixivpy
RUN pip install discord.py

CMD ["python3", "bot.py"]
