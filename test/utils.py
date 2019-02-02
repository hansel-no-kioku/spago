import subprocess
import os.path
import signal
import time
import difflib
import platform

def fail(msg):
    """
    Print a message and exit
    """
    print(msg)
    exit(1)


def call(expected_code, command, failure_msg):
    """
    Try to run a command and exit if fails
    """
    try:
        return subprocess.check_output(command, stderr=subprocess.STDOUT).decode('utf-8')
    except subprocess.CalledProcessError as e:
        if e.returncode == expected_code:
            return e.output.decode('utf-8')
        else:
            print("FAILURE: " + failure_msg)
            print("Program output:")
            fail(e.output.decode('utf-8'))


def expect_success(command, *args):
    print('Expecting success from: "' + ' '.join(command) + '"')
    return call(0, command, *args)


def expect_failure(command, *args):
    print('Expecting failure from: "' + ' '.join(command) + '"')
    return call(1, command, *args)


# Credit: https://stackoverflow.com/questions/4789837/
def run_for(delay, command):
    """
    Run a command and kill it after a certain delay
    """
    print('Going to run this for {}s: "{}"'.format(delay, ' '.join(command)))
    with open(os.devnull, 'w') as FNULL:
        process = subprocess.Popen(command, stdout=FNULL, stderr=FNULL)
        time.sleep(delay)
        if platform.system() == 'Windows':
            process.send_signal(signal.CTRL_C_EVENT)
        else:
            process.send_signal(signal.SIGINT)


def check_fixture(name):
    fixture = '../fixtures/' + name
    with open(name, 'r', encoding='utf-8') as result, \
         open(fixture, 'r', encoding='utf-8') as expected:
        res_lines = result.readlines()
        exp_lines = expected.readlines()
        res_str = ''.join(res_lines)
        exp_str = ''.join(exp_lines)
        if res_str != exp_str:
            print("\nFAILURE: Fixture doesn't match")
            diff = difflib.context_diff(res_lines, exp_lines, fromfile='generated', tofile='expected')
            fail("\nDiff:\n" + ''.join(diff))
        else:
            print('Successfully verified fixture for "{}"'.format(name))
