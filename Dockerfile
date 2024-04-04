FROM ubuntu:latest
RUN apt-get update && apt-get install -y python3-pip && apt-get install cron
COPY /codes/requirements.txt .

COPY /codes/script_manager.sh .

RUN pip3 install -r ./requirements.txt

RUN chmod +x script_manager.sh
CMD ["bash", "script_manager.sh"]
