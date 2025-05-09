# Exercise 7: Services

The goal of this task is to create a Service which matches our previously created Deployment.

Your task is simple: Create a ClusterIP Service that forwards all traffic sent to it to one of its Pods. Your Service should be available at Port 80. Remember that the application listens on Port 8080!

Verify your solution by applying your yaml file to Kubernetes, then running *kubectl get svc* to check that the Service is there.

Additionally, you can do *kubectl describe svc <svc_name>* to get a detailed description of your newly created Service. You should look for the "Endpoints" section: Ideally, you should see 3 IP-addresses there.
Now, do *kubectl get pods -o wide* to show your Pods including their IP-addresses. Verify they are the same as the Endpoints.

You can also verify your solution by running *kubectl port-forward svc/<svc_name> <localhost_port:service_port>*