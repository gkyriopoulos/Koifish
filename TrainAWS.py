#!/usr/bin/env python3
import subprocess
import sys

def run_main_program(board, episodes):
    # Run the Main.py program
    subprocess.call(['python3', 'Trainer.py', board, episodes])

#def commit_changes(token):
    # # Add all changes
    # subprocess.call(['git', 'add', 'RKvsRK.json'])
    
    # # Commit changes
    # subprocess.call(['git', 'commit', '-m', 'Committing changes from script'])
    
    #  # Push changes to GitHub with credentials
    # repo_url = 'https://github.com/JoelJa835/BetaZero.git'
    # url_with_token = f'https://JoelJa835:{token}@{repo_url.split("://")[1]}'
    # subprocess.call(['git', 'push', url_with_token])
    
    
    

def main():
    if len(sys.argv) != 3:
        print("Please provide command-line arguments.")
        return
    
    #token = sys.argv[1]
    board = sys.argv[1]
    episodes = sys.argv[2]
    
    run_main_program(board,episodes)
    #commit_changes(token)

if __name__ == '__main__':
    main()
    
                                                                             
