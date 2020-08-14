from DataBase import DataBaseConnection
import main

import shutil
import os
import glob


"""def recursive_copy_files(source_path, destination_path, override=True):
    files_count = 0

    if not os.path.exists(destination_path):
        os.mkdir(destination_path)
        print('Creating destination directory')
    
    items = glob.glob(source_path + '/*')
    for item in items:
        if os.path.isdir(item):
            path = os.path.join(destination_path, item.split('/')[-1])
            files_count += recursive_copy_files(source_path=item, destination_path=path, override=override)
        else:
            file = os.path.join(destination_path, item.split('/')[-1])
            if not os.path.exists(file) or override:
                shutil.copyfile(item, file)
                files_count += 1
    return files_count

if not (main.VER == DataBaseConnection().GetVersion()):
    
    print(recursive_copy_files('C:\\Users\\renan.klehm\\Desktop\\backup', 'C:\\Users\\renan.klehm\\Desktop\\WM-Lages'))
    main.launch()
else:
    main.launch()"""

main.launch()