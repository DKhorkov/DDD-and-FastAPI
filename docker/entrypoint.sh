#!/bin/bash


if [[ -z "${HOST}" ]]; then
  HOST="0.0.0.0"
else
  HOST="${HOST}"
fi

if [[ -z "${PORT}" ]]; then
  PORT=8000
else
  PORT="${PORT}"
fi

if [[ -z "${WORKERS}" ]]; then
  WORKERS=4
else
  WORKERS="${WORKERS}"
fi

if [[ -z "${WORKER_CLASS}" ]]; then
  WORKER_CLASS="uvicorn.workers.UvicornWorker"
else
  WORKER_CLASS="${WORKER_CLASS}"
fi

if [[ -z "${LOG_LEVEL}" ]]; then
  LOG_LEVEL="info"
else
  LOG_LEVEL="${LOG_LEVEL}"
fi

if [ "$RELOAD" = true ]; then
  gunicorn src.app:app --workers $WORKERS --worker-class $WORKER_CLASS --bind $HOST:$PORT --log-level $LOG_LEVEL --reload
else
  gunicorn src.app:app --workers $WORKERS --worker-class $WORKER_CLASS --bind $HOST:$PORT --log-level $LOG_LEVEL
fi
