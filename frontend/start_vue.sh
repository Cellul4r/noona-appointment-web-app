#!/bin/sh

set -e

APP_MODE="$(printf "%s" "$APP_ENV" | awk '{print $1}')"

if [ -z "$APP_MODE" ]; then
  APP_MODE="development"
fi

if [ "$APP_MODE" = "development" ]; then
  npm install --verbose
  exec npm run dev -- --host 0.0.0.0 --port 8080
elif [ "$APP_MODE" = "production" ]; then
  npm install --verbose
  npm run build
  exec npm run preview -- --host 0.0.0.0 --port 8080
else
  echo "Unsupported APP_ENV value: '$APP_ENV'"
  echo "Use APP_ENV=development or APP_ENV=production"
  exit 1
fi

