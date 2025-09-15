# WSGI entry point for Elastic Beanstalk
# EB looks for 'application' by default; import Flask app as 'application'
from app import app as application
