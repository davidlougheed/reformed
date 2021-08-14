FROM pandoc/latex:2.14.1

LABEL maintainer="David Lougheed <david.lougheed@gmail.com>" \
    org.opencontainers.image.title="reformed" \
    org.opencontainers.image.description="A document format conversion service based on Pandoc." \
    org.opencontainers.image.authors="David Lougheed <david.lougheed@gmail.com>" \
    org.opencontainers.image.licenses="GPLv3"

ENV PYTHONUNBUFFERED 1

RUN apk add --update --no-cache python3 &&  \
    ln -sf python3 /usr/bin/python &&  \
    python3 -m ensurepip &&  \
    pip3 install --no-cache --upgrade pip setuptools

RUN mkdir /reformed/
WORKDIR /reformed/

COPY requirements.prod.txt ./
RUN pip install -r ./requirements.prod.txt

COPY . .
RUN pip install .

EXPOSE 8000

ENTRYPOINT []
CMD [ "python", "-m", "reformed.server" ]
