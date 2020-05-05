import os
import subprocess
from argparse import ArgumentParser

MODULES = ['Proxy', 'Parser', 'Generator', 'WebExport']

def build_image(image_name, dockerfile_folder):
    if subprocess.Popen('docker build -t {} -f {}/Dockerfile .'.format(image_name, dockerfile_folder), shell=True).wait() != 0:
        raise Exception('failed to build docker image for {}'.format(dockerfile_folder))

def run_build():
    for module in MODULES:
        build_image(module.lower() + '_img', module)

def run_schemerator(work_dir, app_url, app_port, ptime):
    try:
        print('you have {} minutes to interact with the proxy in localhost:8080'.format(ptime))
        if subprocess.Popen('docker run -p 8080:8080 -v {}/db:/home/mitmproxy/db -e APP_URL={} -e APP_PORT={} --name proxy proxy_img'.format(work_dir, app_url, app_port), shell=True).wait(ptime * 60) != 0:
            print("error starting proxy")
            return
    except Exception as e:
        subprocess.Popen('docker stop proxy', shell=True)
        subprocess.Popen('docker rm -f proxy', shell=True)
        print("finished proxy")

    for module in MODULES[1:-1]:
        if subprocess.Popen('docker run -v {}/db:/home/db {}'.format(work_dir,module.lower() + '_img'), shell=True).wait() != 0:
            print("error in {}".format(module))
            return

    if subprocess.Popen('docker run -p 8080:8080 -v {}/db:/home/db webexport_img'.format(work_dir), shell=True).wait() != 0:
        print("error in WebExport")
    

def main():
    pars = ArgumentParser()
    pars.add_argument('-b', action='store_true', default=False, help='run build')
    pars.add_argument('-r', type=int, default=0, help='run schemerator')
    pars.add_argument('--url', type=str, default='demo-api-app-git-schemerator.apps.whynot.play.com')
    pars.add_argument('--port', type=str, default='80')

    args = pars.parse_args()
    work_dir = os.getcwd()

    if args.b:
        print("building docker images...")
        run_build()
    if args.r:
        print("running schemerator...")
        run_schemerator(work_dir, args.url, args.port, args.r)

    if not args.b and not args.r:
        print('you is stupid')

if __name__ == "__main__":
    main()
