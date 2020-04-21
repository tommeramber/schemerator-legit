# my-proxy

## INFO
**template.yml** is the template for the users (meaning, the template assumes the container images the schemerator uses are already there)

In the template file I created:
- **Job** - Contains a list of containers to run
- **PersistentVolumeClain** - Persistent volume for the DB
- **Service** - So traffic can enter the proxy
- **Route** - So traffic from outside of OpenShift can get to the proxy




## TODOs

### Dockerfile
1. Use OpenShift's environment variables for the arguments (I started but didn't finish).
2. Write to full command (with arguments) inside the Dockerfile instead of writing them in OpenShift.
3. Re-think the "chmod a+wr" workaround.

### Module
1. Add an exit condition for the proxy (e.g. "After 1000 requests" or "After 48 hours"), make sure it exits with 0 as an exit code (I saw you can use the ctx object for that).
2. Change the path at line 22 to be an argument and not static string.

### Demo-App
1. Change the "put" to the standart way in mod (currently uses query parameters).

### Template
1. Change the image name from "schemerator/my-proxy-git" to a more appropriate name.
2. Add new containers under "objects.spec.template.spec.containers".


## Snippets

To run the app template from your workstation:  
`oc process -f ./template.yaml | oc create -f -`

To delete all the objects that are created by the template:  
`oc delete all configmap/schemerator-app-configmap svc/schemerator-app-proxy-service job/schemerator-app-job pvc/schemerator-app-db-pvc route/schemerator-app-proxy-route`



To run the dev template from your workstation:  
`oc process -f ./def-template.yaml | oc create -f -`

`oc delete all -l template=schemerator-dev-template`
does not delete secrets!

## Run Localy
In the dockerfile location : 
`docker image build .`

`docker run -v {DB_LOCAL_FOLDER}:/home/mitmproxy/db --env APP_URL={DEMO_APP_URL} --env APP_PORT=80 -p 8080:8080 {IMAGE_HASH}`