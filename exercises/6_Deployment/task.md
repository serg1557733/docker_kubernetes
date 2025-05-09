# Exercise 6: Creating a deployment

Our app is quickly rising in popularity, and a single Pod won't cut the increasing load! Thus, we want to create multiple Replicas of our application. 

Create a deployment.yaml File which creates 3 of our previously defined Pods, then, apply it to our Cluster. 

Verify your solution by running: 

- *kubectl get deploy*
- *kubectl get rs* 
- *kubectl get pods*

You can also access your deployment's Pods in your browser by running  *kubectl port-forward deploy/<deployment_name> <localhost_port:service_port>*