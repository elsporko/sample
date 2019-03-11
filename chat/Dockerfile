FROM python:3-onbuild

ARG secret=SECRET
ENV aws_secret_access_key=${secret}

ARG key=KEY
ENV aws_access_key_id=$key

ARG default=DEFAULT
ENV aws_default_region=$default

CMD ["python3", "./client.py"]

#====================================
#ARG buildtime_variable=default_value
#ENV env_var_name=$buildtime_variable
#When you’re building your image, you can override the default_value directly from the command line:
#
#$ docker build --build-arg buildtime_variable=a_value # [...]
