#!/bin/bash
isort --settings-file tool/.isort.cfg .
black --config tool/.black . 
flake8 --config tool/.flake8 .