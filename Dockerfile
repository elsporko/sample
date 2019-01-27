FROM python:3-onbuild

ARG secret=SECRET
ENV AWS_SECRET_ACCESS_KEY=${secret}

ARG key=KEY
ENV AWS_ACCESS_KEY_ID=$key

ARG default=DEFAULT
ENV AWS_DEFAULT_REGION=$default

CMD ["python", "./client.py"]

#====================================
#ARG buildtime_variable=default_value
#ENV env_var_name=$buildtime_variable
#When you’re building your image, you can override the default_value directly from the command line:
#
#$ docker build --build-arg buildtime_variable=a_value # [...]
