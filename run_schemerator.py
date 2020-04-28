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

def run_schemerator(work_dir):
    try:
        print('you have 3 minutes to interact with the proxy in localhost:8080')
        subprocess.Popen('docker run -p 8080:8080 -v {}/db:/home/mitmproxy/db -e APP_URL=172.20.10.2 -e APP_PORT=8082 --name proxy proxy_img'.format(work_dir), shell=True).wait(180)
    except Exception as e:
        subprocess.Popen('docker stop proxy', shell=True)
        print("finished proxy")

    for module in MODULES[1:-1]:
        subprocess.Popen('docker run -v {}/db:/home/db {}'.format(work_dir,module.lower() + '_img'), shell=True).wait()

    subprocess.Popen('docker run -p 8080:8080 -v {}/db:/home/db webexport_img'.format(work_dir), shell=True).wait()
    

def main():
    pars = ArgumentParser()
    pars.add_argument('-b', action='store_true', default=False)
    pars.add_argument('-r', action='store_true', default=False)
    
    args = pars.parse_args()
    work_dir = os.getcwd()

    if args.b:
        print("building docker images...")
        run_build()
    if args.r:
        print("running schemerator...")
        run_schemerator(work_dir)

if __name__ == "__main__":
    main()
