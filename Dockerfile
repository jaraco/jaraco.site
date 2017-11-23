FROM python:3

RUN apt update && apt install -y fop
COPY . /repo
RUN pip install /repo
ENV PORT=80
EXPOSE 80

CMD python -m cherrypy -i jaraco.site.run
