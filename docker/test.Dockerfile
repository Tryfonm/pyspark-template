FROM tryfonm/spark-node

WORKDIR /workspace
COPY . /workspace

# RUN source ./venv/bin/activate

# ENTRYPOINT ["tox"]