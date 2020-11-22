FROM sl_base

COPY backend/requirements-dev.txt ./
RUN pip install -r requirements-dev.txt