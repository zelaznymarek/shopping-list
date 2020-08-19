FROM sl_base

COPY requirements-dev.txt ./
RUN pip install -r requirements-dev.txt