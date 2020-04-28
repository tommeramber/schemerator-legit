import os
import subprocess

MODULES = ['Proxy', 'Parser', 'Generator', 'WebExport']


def build_image(image_name, dockerfile_folder):
    if subprocess.Popen('docker build -t {} -f {}/Dockerfile .'.format(image_name, dockerfile_folder), shell=True).wait() != 0:
        raise Exception('failed to build docker image for {}'.format(dockerfile_folder))

def run_build():
    for module in MODULES:
        build_image(module.lower() + '_img', module)

def run_schemerator():
    try:
        print('you have 3 minutes to interact with the proxy in localhost:8080')
        subprocess.Popen('docker run -p 8080:8080 -v /Users/alonamovshovich/Documents/Work/Schemerator/schemerator/db:/home/mitmproxy/db -e APP_URL=172.20.10.2 -e APP_PORT=8082 --name proxy proxy_img', shell=True).wait(180)
    except Exception as e:
        subprocess.Popen('docker stop proxy', shell=True)
        print("finished proxy")

    for module in MODULES[1:-1]:
        subprocess.Popen('docker run -v /Users/alonamovshovich/Documents/Work/Schemerator/schemerator/db:/home/db {}'.format(module.lower() + '_img'), shell=True).wait()

    subprocess.Popen('docker run -p 8080:8080 -v /Users/alonamovshovich/Documents/Work/Schemerator/schemerator/db:/home/db webexport_img', shell=True).wait()
    

def main():
    os.chdir('/Users/alonamovshovich/Documents/Work/Schemerator/schemerator/')
    run_build()
    run_schemerator()

if __name__ == "__main__":
    main()
