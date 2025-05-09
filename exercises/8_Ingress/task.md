# Exercise 8: Ingress

## Preparation

Since minikube is merely a small, local installation of Kubernetes it can't compete with, say, OpenShift for "Enterprise functionality". So, we have to make a couple preparations in order to get Ingress working. Execute the following commands:

1. minikube addons enable ingress
2. minikube addons enable ingress-dns 
3. kubectl get pods -n ingress-nginx
4. minikube tunnel (this will block your shell, you will need a new one!)

Now, since we want to make use of DNS-Names for Ingress, we need to create some local ones that point to minikube, which is now available on localhost.

Open the hosts-File in C:\Windows\System32\drivers\etc  as administrator and add the following line to it:

127.0.0.1   kubernetestraining.com

## Task 

The task itself is *rather* simple: Create an Ingress Object that allows us to open kubernetestraining.com in our browser and see our application!

Tip: You can get "Sceleton" yaml-Files in the Kubernetes Documentation.