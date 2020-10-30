#### run robovetter
./robovet kplr_dr25_obs_robovetter_input.txt test_output.txt 10000

#### unzip files
tar xvzf [filename]

### utilities
#### allocating different running tasks to different cpus
ps -af (gets list of running processes)
use kill [pid] to stop a process
taskset -p [pid] tells you which CPU that process is using
taskset -p 2 [pid] sets that process to that cpu
so would take the 2nd, 3rd and 4th python processes and taskset -p to 2, 3 and 4.
I think is numbered 0 to 3
so taskset -c 2 python3 make_dataset1.py puts it on CPU #3 
or taskset -c 2 nohup python3 make_dataset1.py with nohup

nohup python3 make_dataset1.py
taskset -c 1 nohup python3 make_dataset2.py
taskset -c 2 nohup python3 make_dataset3.py
taskset -c 3 nohup python3 make_dataset4.py

#### jupyter
jupyter notebook --port=8886
jupyter notebook list
jupyter notebook stop



#### cpu and memory utilization
htop
nmon


### gpu vm
ssh -i /Users/travismetz/Dropbox/DesktopFolder/aws/trm-private-key.pem ubuntu@ec2-3-138-171-160.us-east-2.compute.amazonaws.com

ssh -L localhost:8888:localhost:8888 -i /Users/travismetz/Dropbox/DesktopFolder/aws/trm-private-key.pem ubuntu@ec2-3-138-171-160.us-east-2.compute.amazonaws.com

### v3 vm

ssh -i /Users/travismetz/Dropbox/DesktopFolder/aws/trm-private-key.pem ubuntu@ec2-3-23-23-2.us-east-2.compute.amazonaws.com

ssh -L localhost:8886:localhost:8886 -i /Users/travismetz/Dropbox/DesktopFolder/aws/trm-private-key.pem ubuntu@ec2-3-23-23-2.us-east-2.compute.amazonaws.com

### v2 vm

ssh -i /Users/travismetz/Dropbox/DesktopFolder/aws/trm-private-key.pem ubuntu@ec2-3-14-124-166.us-east-2.compute.amazonaws.com

ssh -L localhost:8888:localhost:8888 -i /Users/travismetz/Dropbox/DesktopFolder/aws/trm-private-key.pem ubuntu@ec2-3-14-124-166.us-east-2.compute.amazonaws.com



conda env list
source activate []


source activate tensorflow2_latest_p37

#### directory structure
tree -o [filename] -n
-n turns off color codes in text file

find . -name '*.fits' -type f -delete

   
