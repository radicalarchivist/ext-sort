import os
import shutil

def diff_path(file_dir,scan_dir):
    return file_dir.replace(scan_dir,"")

def get_filelist(path,exts,recurse):
    abspath = os.path.abspath(path)
    retlist = []
    if not recurse:
        for item in os.listdir(abspath):
            if os.path.isdir(os.path.join(path,item)):
                continue
            if item.split('.')[-1] in exts:
                retlist.append(os.path.join(path,item))
    else:
        for root,dirs,files in os.walk(abspath):
            for name in files:
                if name.split('.')[-1] in exts:
                    retlist.append(os.path.join(root,name))
    return retlist

def move_files(filelist,source,destination,keep_structure):
    for path in filelist:
        if keep_structure:
            target = os.path.join(destination,diff_path(path,source))
        else:
            _, name = os.path.split(path)
            target = os.path.join(destination,name)
        try:
            tPath, _ = os.path.split(target)
            try:
                os.makedirs(tPath,exist_ok=True)
            except Exception:
                print("Unable to create the target directory. Do you have the correct permissions?")
                exit(1)
            print(f"{path} --> {target}")
            shutil.move(path,target)
        except Exception as e:
            print(f"There was a problem moving the file: {e}")
            exit(1)

def yn_prompt(prompt: str):
    '''
    Yes or no prompt
    '''
    while True:
        try:
            answer = input(f"{prompt} (y/[n]) ")
            if answer[0] == 'y' or answer[0] == 'n':
                if answer[0] == 'y':
                    return True
                else:
                    return False                    
            else:
                raise ValueError
        except ValueError:
            print('You must enter y or n.\n')
        except IndexError:
            return False