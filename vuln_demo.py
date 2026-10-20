import subprocess


def run_command(user_input):
    return subprocess.call(user_input, shell=True)