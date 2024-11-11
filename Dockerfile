FROM python


WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt


# CMD [ "python", "./your-daemon-or-script.py" ]
ENTRYPOINT [ "./run.sh" ]
