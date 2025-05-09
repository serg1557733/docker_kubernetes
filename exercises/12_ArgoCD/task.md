# Exercise 12: ArgoCD

Finally, let's roll out our Application using a GitOps-Tool called ArgoCD. GitOps tools provide a declarative way to describe *how* you want your software to be deployed.

## Preparation

First, we need to roll out ArgoCD. You can check the general instructions for Linux / Mac here, but we will use our own, since we are on Windows:

You have to execute the following: 

1. kubectl create namespace argocd
2. kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
3. kubectl patch svc argocd-server -n argocd -p '{"spec": {"type": "LoadBalancer"}}'
4. kubectl get secret argocd-initial-admin-secret -n argocd -o jsonpath="{.data.password}" | base64 --decode
5. kubectl port-forward svc/argocd-server -n argocd 8080:443

Now, you can open http://localhost:8080 and login to ArgoCD using the "admin" user and the output from step 4 as your password!

Also, uninstall your "old" Helm-Chart using *helm uninstall <chart_name>*
## Task

Add a new Application to ArgoCD using the "New App" Button in the Top Left Corner.

1. Set the Application Name and Project Name. Set the Sync Policy to "Automatic" and check the boxes "Prune Resources" and "Self Heal".
2. Set the Repository URL to https://github.com/helm/examples and wait a couple seconds. Click on "Path", you should be able to select "charts/hello-world" now.
3. Set the Cluster URL to the only available option and the Namespace to "default"
4. You should see the available Helm-Values if you scroll down. Try changing the replicaCount to 3.
5. Click on "Edit as YAML" in the top right corner and look at what you see. You can also write your "Application" as a YAML-File, which is the recommended way of using ArgoCD (Infrastructure as Code). We will stick to the UI for now, but what we set before can be seen here aswell.
6. Click "Create" in the top left corner.
7. Click on your Application and get used to the UI.

OPTIONAL CHALLENGE: Try pushing your new Helm-Chart to our Cluster using ArgoCD. The general steps are the same as above, BUT: You first have to publish your Helm-Chart somewhere. To do so, create a public Git(-Hub, -Lab, ...)-Repository and Upload your Helm-Chart to it. Now, you only need to swap out the URL from step 2 to your Git-Repository. :)


## Verification

You should now be able to see the application in your Cluster. Check it using the usual commands: *kubectl get pods* and so on...