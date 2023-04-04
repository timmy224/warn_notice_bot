FROM public.ecr.aws/lambda/python:3.8

COPY requirements.txt  .
RUN  pip3 install -r requirements.txt --target "${LAMBDA_TASK_ROOT}"

COPY . ${LAMBDA_TASK_ROOT}
COPY warn_classes/ ${LAMBDA_TASK_ROOT}/warn_classes/

CMD [ "main.handler" ]