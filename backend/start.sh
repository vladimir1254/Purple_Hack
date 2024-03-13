#!/bin/bash
cd /usr/src/app && uvicorn main:app --host 0.0.0.0 --port 5000 --reload;