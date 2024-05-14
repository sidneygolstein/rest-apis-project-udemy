"""
Script running when the docker file is running, i.e., when render.com runs our containers)
File that needs to: 
   Run the migration 
   Start the gunicorn process
"""

#!/bin/sh

flask db upgrade

exec gunicorn --bind 0.0.0.0:80 "app:create_app()"