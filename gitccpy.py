import os
import sys
import subprocess
import shutil

CURRENT_PATH = os.getcwd().replace("\\", "/")

COMMIT_ID = 'HEAD'

CONFIGS = {
    'LOCAL_PREXFIX' : '',
    'DESTINATION_PATH' : None
}

######################################## [read args]

if len(sys.argv) > 1:
    params = sys.argv[1:]
    COMMIT_ID = params[0]

######################################## [read .gitccpy]

if not os.path.isfile(CURRENT_PATH + '/' + '.gitccpy'):
    print('.gitccpy not found!')
    exit()

with open(CURRENT_PATH + '/' + '.gitccpy', 'r') as f:
    for line in f.readlines():
        kv = [s.strip() for s in line.split('=')]
        CONFIGS[kv[0]] = kv[1]

if CONFIGS['DESTINATION_PATH'] == None:
    print('DESTINATION_PATH is not defined in .gitccpy')
    exit()

######################################## [functions]

copied_count = 0

def clear_destination(folder):
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))

def cp(from_path, to_path):
    if not os.path.isfile(from_path): return
    os.makedirs(os.path.dirname(to_path), exist_ok=True)
    f1 = open(from_path, 'rb')
    f2 = open(to_path, 'wb')
    f2.write(f1.read())
    f1.close()
    f2.close()

def copy_paths(paths):
    global copied_count

    for p in paths:
        if (not p.startswith(CONFIGS['LOCAL_PREXFIX'])): continue
        copy_from = CURRENT_PATH + '/' + p
        copy_to = CONFIGS['DESTINATION_PATH'] + '/' + p.replace(CONFIGS['LOCAL_PREXFIX'], '')
        print("copying...", copy_from)
        cp(copy_from, copy_to)
        copied_count += 1

######################################## [execute git diff-tree]

git_command = ['git', 'diff-tree', '--no-commit-id', '--name-only', '-r', COMMIT_ID]

result = subprocess.run(git_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

if result.returncode == 0:
    paths = result.stdout.splitlines()
    
    clear_destination(CONFIGS['DESTINATION_PATH'])
    copy_paths(paths)

    if copied_count == 0:
        print('No changes in ', CONFIGS['LOCAL_PREXFIX'])
    else:
        print(copied_count, "files copied into", CONFIGS['DESTINATION_PATH'])
else:
    print("Error executing git diff-tree command:")
    print(result.stderr)
