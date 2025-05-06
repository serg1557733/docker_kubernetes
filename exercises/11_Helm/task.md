# Exercise 11: Helm

Let's package our application as a "Helm Chart"!

## Task

The task is simple: Take all the Objects (Deployments, Services, Volumes...) that you created earlier and package them into a Helm Chart!

1. To create the "base structure", use $ helm create my-app
2. Then, carry over your Environment into the templates folder. If you feel brave, you can also try to put some Variables into the values.yaml-File. For example, you could make your ConfigMap configurable from the Values-File by replacing the ENV-Variable in the ConfigMap with some {{ .Values... }} reference. 
3. Delete all Deployments, ConfigMaps, Services, Ingress Rules and PVCs (in that order!)
4. Go to the "Base-Directory" of the Helm Chart (the one with the Chart.yaml in it) and install your Helm-Chart using Chart using $ helm install my-app . 

## Verification

If everything went right, you should see the same infrastructure as before, just rolled out "at once" using Helm!