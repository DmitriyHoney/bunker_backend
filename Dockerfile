FROM python:latest

WORKDIR /backend

RUN apt update && DEBIAN_FRONTEND=noninteractive \
        apt-get update && apt-get install -y --no-install-recommends \
            libmpc-dev \
            libgmp-dev \
            libmpfr-dev

RUN pip install --no-cache-dir --upgrade pip setuptools

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# RUN poetry install

RUN chmod +x entrypoint.sh
CMD ["/bin/bash", "./entrypoint.sh"]
