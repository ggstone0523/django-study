import os

if os.system("docker build -t mysite .") != 0:
    exit
os.system("docker run -dp 8000:8000 --name simplepolls mysite")
