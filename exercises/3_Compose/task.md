# Exercise 3: Building Multi-Container Apps using Compose

In this task, we want to combine everything of what we've learned previously to create an environment that's a _little_ more complicated.

Our previously built image also has the ability to connect to a Redis-Database using a connection string which can be configured using the REDIS_URL environment variable. If there is a Redis-DB to connect to, our application will display an option to view and alter Key-Value pairs in it.

## Building the compose file

Our goal is to create a Docker-Compose file which includes the following:

- A Redis-DB (using the redis image and the service-name` redis), which listens on Port 6379
- A volume for the Redis-DB, which is mapped to the Redis containers /data path
- Our application, which should be available on localhost Port 8080 and be built automatically from our Dockerfile
- The above mentioned REDIS_URL environment variable set to: "redis://<redis_service_name>:<redis_port>"

## Running and testing the file

To confirm that your file is working, run _docker compose up_ and add some Key-Value-Pairs after opening the Website. Then, kill the compose-environment using _docker compose down_ and restart it again. Your added data should still be displayed.

## Bonus Points

In this repository, you will notice there is also a directory called /images/ which contains a cat.
Try mounting this directory to the directory /app/images/ in your container and see what happens after you restart your environment.
