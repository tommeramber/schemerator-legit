### Schemerator commands
oc create -f proxy_template.yml
oc process \
-p PROXY_IMAGE=quay.io/tamber/schemerator-proxy:latest \
-p PVC_NAME=XXXXXXXXXXXXX
-p APP_URL=XXXXXXXXXXXXX
-p APP_PORT=XXXXXXXXXXX