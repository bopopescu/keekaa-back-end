#!/bin/sh

echo "Unit Test has been run to make sure all the modules are working. 

The following is the report."

python manage.py test brands actions
