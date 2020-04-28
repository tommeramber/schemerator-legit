FROM mitmproxy/mitmproxy:5.0.1

COPY --chown=mitmproxy Proxy/saveFlow.py "/home/mitmproxy/saveFlow.py"

RUN    mkdir /home/mitmproxy/db \
    && mkdir /home/mitmproxy/mitmconf \
    && chown -R mitmproxy:mitmproxy "/home/mitmproxy/" \
    && chmod a+wr /home/mitmproxy/db \
    && chmod a+wr /home/mitmproxy/mitmconf 
# We need to chmod a+wr because openshift starts the container with a random user (this is my workaround)

# This might not be needed
USER mitmproxy

# CMD is required instead of ENTRYPOINT - overrides the base image ENTRYPOINT for our usecase
# APP_URL and APP_PORT are both env. vars. which will be loaded into the image via ConfigMap within openshift
 
CMD mitmdump --mode reverse:http://${APP_URL}:${APP_PORT} --set confdir=/home/mitmproxy/mitmconf -s /home/mitmproxy/saveFlow.py




# I ran the proxy with the following argumets:
# "mitmdump mode reverse:http://${APPLICATION-URL}:${APPLICATION-PORT} --set confdir=/home/mitmproxy/mitmconf -s /home/mitmproxy/saveFlow.py"
# Explaination:
# [mitmdump] - using "mitmproxy" requires tty so it can't run in openshift, mitmdump works.
# [reverse:URL] - For making mitmdump run using 
# [--set confdir=/home/mitmproxy/mitmconf] - The default dir is /home/mitmconfig/.mitmconfig but it is owned by root, so i created a new dir, I didn't try to use the default dir after adding "chmod a+wr" so this might be unnecessary.
# [-s /home/mitmproxy/saveFlow.py] - Load our module.

# Add-ons:
# 1. Pre-deloyment: Add ConfigMap which contains APP_URL as the svc-name of the api which will be redirected by the mitmproxy + port in APP_PORT
# 2. Post-deployment: 
    # add voulme for db:
    # 2.1. oc get dc/<mitmproxy_deploymentConfigruation> -o yaml > out.yml
    # 2.2. edit the yaml file - add volum mount + volumes (volumeClaim name)
    # 2.3. oc replace -f out.yml ==> will replace the previous dc with the new one that containes the pvc + mount point

