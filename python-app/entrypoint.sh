#!/usr/bin/env bash

set -e
. $(pipenv --venv)/bin/activate
exec "$@"
