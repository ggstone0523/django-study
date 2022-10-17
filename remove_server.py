import os

if os.system("docker stop simplepolls") != 0:
    exit
if os.system("docker rm simplepolls") != 0:
    exit
os.system("docker rmi mysite")
