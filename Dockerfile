FROM python:3.11.4-alpine as base
FROM base as builder

COPY requirements.txt /requirements.txt
RUN apt-get install build-essential -y
RUN pip install --user -r /requirements.txt

FROM base
WORKDIR /base

COPY --from=builder /root/.local /root/.local
COPY ./hypixel_chinese_skyblock_bot ./bot

ENV PATH=/root/.local:$PATH

CMD ["python", "-m", "bot"]
