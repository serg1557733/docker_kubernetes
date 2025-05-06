# Exercise 10: ConfigMap

As was said before, we are lastly going to configure our App with the REDIS_URL Variable to connect to our Redis instance.

## Task 

1. Create a ConfigMap containing the Environment variable! The Redis connection string should have the following form: "redis://<redis_service_name>:6379". Don't forget to apply it to our Cluster.
2. Take our App Deployment file from the exercise 6 and change it up to include your newly created CM. Update your Deployment.

## Verification

Now, to make sure everything is working fine now, open up your App using it's URL and check to see if the "Redis stuff" is there.