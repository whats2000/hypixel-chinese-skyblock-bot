FROM python:3.9-slim as base
FROM base as builder

# Install build dependencies
RUN apt-get update && apt-get install -y gcc

COPY requirements.txt /requirements.txt
RUN pip install --user -r /requirements.txt

FROM base
WORKDIR /base

COPY --from=builder /root/.local /root/.local
COPY ./hypixel_chinese_skyblock_bot .

ENV PATH=/root/.local:$PATH


CMD ["python", "__main__.py"]
