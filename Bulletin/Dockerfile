FROM python:3.10

WORKDIR /usr/src/app

ENV PATH /usr/src/app:$PATH

COPY send_bulletin.py /usr/src/app/send_bulletin.py
COPY required.txt /usr/src/app/required.txt
COPY run.sh /usr/src/app/run.sh

RUN pip install --user -r required.txt

RUN chmod a+x /usr/src/app/run.sh

ENTRYPOINT ["bash", "-c"]
# ENTRYPOINT ["/usr/src/app/run_py.sh"]

