FROM python:3
RUN apt-get update
RUN apt install -y libgl1-mesa-glx
COPY . .
RUN pip install -r requirements.txt
CMD [ "python", "./bot.py" ]