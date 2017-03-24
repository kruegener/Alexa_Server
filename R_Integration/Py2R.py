import subprocess

command = 'Rscript'
path2script = 'max.R'

args = ['11', '12', '35']

cmd = [command, path2script] + args

x = subprocess.check_output(cmd, universal_newlines=True)

print('The max of the numbers is:', x)
