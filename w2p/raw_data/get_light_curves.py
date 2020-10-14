import subprocess
import os
import time

def get_size(start_path = '.'):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(start_path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            # skip if it is symbolic link
            if not os.path.islink(fp):
                total_size += os.path.getsize(fp)

    return total_size

print(os.listdir())
print('creating batch file')
os.system("python3 make_light_curve_batch.py -o light_curves/get_kepler.sh")
print('done creating batch file')

startTime = time.time()
print ("starting batch file")
subprocess.call("light_curves/get_kepler.sh")
print ("ending batch file")
executionTime = (time.time() - startTime)
print('Execution time in seconds: ' + str(executionTime))


print('KB of light_curves:',get_size('light_curves/'), 'bytes')