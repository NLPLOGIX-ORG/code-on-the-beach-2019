docker stop codeonthebeach2019notebook
docker rm codeonthebeach2019notebook

docker run -p 8888:8888 -d -v %CD%\notebook:/home/jovyan/work --name codeonthebeach2019notebook jupyter/datascience-notebook
docker logs -f codeonthebeach2019notebook