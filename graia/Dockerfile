FROM  python:3.7
  
WORKDIR  /app
  
RUN  pip install pyyaml graia-application-mirai -i https://mirrors.aliyun.com/pypi/simple/ 

# Run app.py when the container launches
CMD ["python", "main.py"]
