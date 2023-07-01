#!/usr/bin/env python3
import sys
import subprocess

def main():
    if len(sys.argv) != 4:
        print("Please provide the personal access token as a command-line argument.")
        return
    
    dir1 = '/train_data'
    dir2 = '/stats'
    
    key = sys.argv[1]
    instance = sys.argv[2]
    dw = sys.argv[3]
    
    instance_dir1 = instance + dir1 + '/*'
    instance_dir2 = instance + dir2 + '/*'
    dw_dir1 = dw + dir1
    dw_dir2 = dw + dir2
    
    instance_dirs = [instance_dir1, instance_dir2]
    dw_dirs = [dw_dir1, dw_dir2]
    
    for i in range(len(instance_dirs)):
        subprocess.call(['sudo', 'scp', '-i', key, instance_dirs[i], dw_dirs[i]])
    

if __name__ == '__main__':
    main()
    
    
    #sudo scp -i "python-web-server.pem" ec2-user@ec2-13-53-131-250.eu-north-1.compute.amazonaws.com:/home/ec2-user/train_data/test* /home/jogopogo/Projects/Koifish/