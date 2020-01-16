import subprocess


def execute_in_virtualenv(venv_name, file):
    print(subprocess.run(["{0}/bin/python".format(venv_name), file]))


if __name__ == "__main__":
    execute_in_virtualenv(".venv", "cv2debugger.py")
