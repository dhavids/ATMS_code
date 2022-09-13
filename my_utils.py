import os
import shutil
import time
from shutil import unpack_archive, make_archive

#import pyfastcopy
'''
unzip_file(archive_dir, target_dir= None, format= 'zip')
To unzip a file into the current folder it is or another dir 
format can be “zip”, “tar”, “gztar”, “bztar”, or “xztar”
'''
def unzip_file(archive_dir, target_dir= None, format= 'zip'):

  base, archive_name= os.path.split(archive_dir)
  archive_fldr, ext= os.path.splitext(archive_name) 

  #check if file exists, if not supplied, create dir in archive dir
  if target_dir is None:
    target_dir= os.path.join(base, archive_fldr)

  if not os.path.isdir(target_dir):
    os.mkdir(target_dir)
    print('[INFO] Directory created')

  #extract archive with shutil use
  print('[INFO] Extracting...\n')
  unpack_archive(archive_dir, target_dir, format)
  print(f'[INFO] \'{archive_name}\' extracted succesfully into:\n==>{target_dir}')

  # to make archive with shutil
  #make_archive('archive_name', 'format-(zip,tar)', 'root_dir')

#This function accepts a time value and its unit
#and prints it out or returns it as a var
# It can be supplied as raw or rounded
def get_time(since, unit='ms', raw_out=False, info=None):
 
  now = time.time()
  elapsed = now - since
 
  if unit == 'ns':
    elapsed = elapsed * 1000000000
 
  elif unit == 'sec':
    elapsed = elapsed
  
  elif unit == 'us':
    elapsed= elapsed * 1000000
  
  elif unit== 'ms':
    elapsed= elapsed * 1000

  if info:
    print(f'@{info}: ')  

  if raw_out:
    elapsed = elapsed
    print(f'Elapsed time is {elapsed}')
    return elapsed

  else:
    print(f'Elapsed time is {round(elapsed)} {unit}')
    return round(elapsed)
#This allows you to specify the time unit from the begining
#Require you to pass the returned value into get_time as *value (passing a list)
def start_timer(unit = 'ms'):
 
  timer = time.time()
  time_param = [timer, unit]
  return time_param


#To duplicate or backup a dataset
#parent folder to dataset to be copied

def dataSetFldrBkup(dataset, dsc= None):

  if dsc is not None:
    dsc = dsc
  
  else:
    dsc= source + '-copy'
    # check if the dsc dir exist, remove it
    if os.path.isdir(dsc):
      shutil.rmtree(dsc)
      os.mkdir(dsc)

  #start copy operations
  #print dir contents before copying
  print(f'Dirs in parent folder \'{dataset}\' are:')
  print(*os.listdir(dataset), sep='\n', end='\n')

  #grab returned destination foldername
  shutil.copytree(dataset, dsc)

  #print dir contents after copying
  print(f'\nDirs in backup folder \'{dsc}\' are:')
  print(*os.listdir(dataset), sep='\n', end='\n')
  #print(des)


# count number of files and dirs in a given folder path
# Nos of files with a specific extension can also be counted
def analyzeDir(target_dir= None, exts= None):
    
    filepaths= []

    if target_dir is None:
      target_dir= os.getcwd()

    if not os.path.isdir(target_dir):
      print(f'\n[INFO] \'{target_dir}\' is not a Dir. Skipping')
      return

    files = folders = all = count = 0
    report = []
    for path, dirs, elems in os.walk(target_dir):
      folders = len(dirs)
      files= len(elems)
      all= files + folders
      report= files, folders, all

      if exts is not None:
        for elem in elems:
          #os.path.splitext() returns two outputs, 
          #ext is the second
          base, ext= os.path.splitext(elem)

          #increment the number of files and filename list
          if ext in exts:
            filename= (os.path.join(path, elem))
            filepaths.append(filename)
            count += 1

      break
    
    print(f'\n[INFO] In dir \'{target_dir}\', we have:')
    print(f'====>> Files: {files}, Folders: {folders}, All:{all}')

    if exts:
      print(f'====>> {exts} files: {count}\n')
      
    return list(report), filepaths
    
    
#To remove a particular directory tree or file
def removeFileOrDir(dir_to_rem):

  if dir_to_rem is None:
    raise Exception('[ERR] Pls specify a directory/ file to remove')
    return
    
  if not os.path.isdir(dir_to_rem) and not os.path.isfile(dir_to_rem):
    print(f'[WARN] Cannot remove. Dir or File does not exist')
    pass
  
  elif os.path.isfile(dir_to_rem):
    os.remove(dir_to_rem)
    print(f'[INFO] File \'{dir_to_rem}\' removed')

  else:
    shutil.rmtree(dir_to_rem)
    print(f'[INFO] Dir \'{dir_to_rem}\' removed')


#to copy files of a particular extension type 
#form the src_dir or source dirtree into the target dir
#It should be noted that other dirs in the dir to exclude are not scanned too
def copyByExts(src, target= None, exts= None, paths_to_exclude= None,
               one_fldr= False):

  if target is None:
    raise Exception('[ERROR] Pls specify target directory')
  
  # if dir doesnt exist, create it
  if not os.path.isdir(target):
      os.mkdir(target)
      print('[INFO] Directory created\n')
    
  count = 0
  target_old= 0
  for path, dirs, files in os.walk(src):
      #check if path or dirtree is in the specified paths to exclude list
      #if count == 8000:
        #target_old= target 
        #target = '/content/drive/My Drive/dataset/vehicles/raw-stnfd-2'
      #  os.mkdir(target)
      #  print('[INFO] Directory created\n')

      skip_path= False
      
      if paths_to_exclude is not None:

        for paths in paths_to_exclude:
          found= path.find(paths)

          #set the skip_path if the path string exists in paths_to_exclude
          if found != -1:
            skip_path = True

      #if path or dirtree is in current path, skip
      if skip_path:
          print(f'[INFO] Dir \'{path}\' skipped\n')

      #scan the path and copy the matched files
      else:
        print(f'[INFO] Current dir is:\n====>> {path}')
        local_cnt = 0

        for items in files:
          #os.path.splitext() returns two outputs, 
          #ext is the second. base is very important
          base, ext= os.path.splitext(items)

          if ext in exts:
            img_path= os.path.join(path, items)
            dsc= os.path.join(target, items)
            shutil.copyfile(img_path, dsc)
            local_cnt += 1
            count += 1
        
        #if one_folder is set, break the loop
        if one_fldr:
          break

        #print the folder level report and continue
        else:    
          print(f'[INFO] {local_cnt} {exts[0]} and {exts[1]} files '
               f'found here and copied. \n')

  #print the final report of the images found and copied
  print(f'[INFO] Total of {count} {exts[0]} and {exts[1]} files were found in -{src}')
  print(f'[INFO] Copied to: {target}')
  #analyze the target directory
  #analyzeDir(target_old,exts)
  analyzeDir(target,exts)


#function to generate a list of dirspaths to be excluded
def genDirToExclude(dirnames, sub_dirnames= None):
  exclude= []

  for dir in dirnames:
    #check if common subdirs were passed
    if sub_dirnames is not None:
      
      #add them to the parent dir
      for subdir in sub_dirnames:
        subd= os.path.join(dir, subdir)
        exclude.append(os.path.join(dataset_dir, subd))

    #if not, add the original dir only
    else:
      exclude.append(os.path.join(dataset_dir, dir))
  
  return exclude


#to download from a given string link to the downloads folder
#or another specified folder
def downloadFrom(link, dst= 'downloads'):

  if dst == 'downloads':
    dst= r'/content/drive/My Drive/Downloads'

  else:
    if not os.path.isdir(dst):
      os.mkdir(dst)
      print(f'New dir \'{dst}\' created!')

  cwd= os.getcwd()
  os.chdir(dst)
  #download form the link
  #!wget $link
  os.chdir(cwd)

  import os

#make a directory even if the parents does not exists
#it recursively scans the dir name and creates all needed dirs
def mkDir(base_dir):

  def check_and_make_dir(base):
    if not os.path.isdir(base):
      tree, dir= os.path.split(base)
      
      if not os.path.isdir(tree):
        check_and_make_dir(tree)
      
      os.mkdir(base)

  if not os.path.isdir(base_dir):
    check_and_make_dir(base_dir)
    print(f'[INFO] Dir \'{base_dir}\' created\n')

  else:
    print(f'[WARN] Dir \'{base_dir}\' exists\n')
    pass
  return base_dir

#turn a python path str to unix workable path
#The new path must be wrapped in {} to be usable with shell commands
def make_unix_path(base, cd= False):
  '''
  Turn a pathlike python string into one acceptable by the terminal
  major transformation is the addition of a '\' before all ' '
  the new path must be wrapped in {} before being passed to shell
  '''
  path2= ''
  #split accept and uses the ' ' as the default separator
  strs= base.split()
  #join adds all the strs together and includes the joiner admist them
  path2= '\\ '.join(strs)

  if cd:
    os.chdir(base)
    print(os.getcwd())
  
  return path2

#Testl levels
#to find specific filetype by extension in a folder tree
#and copy them all to a new folder
'''
dataset_dir = '/content/drive/My Drive/dataset/vehicledetected-stanford-cars-data-classes-folder'
target_dir = '/content/drive/My Drive/dataset/vehicles/raw-stnfd'
#test='/content/drive/My Drive/dataset/vehicle-data-set-copy/cardataset'
# to first remove the target directory uncommnet here
#data=['test', 'train']
#files= ['Ambulance', 'Barge', 'Bicycle', 'Boat', 'Bus', 'Car', 'Cart', 'Caterpillar', 'Helicopter', 'Limousine', 'Motorcycle', 'Segway', 'Snowmobile', 'Tank', 'Taxi', 'Truck', 'Van']
#for dat in data

#analyzeDir(target_dir)

removeFileOrDir(target_dir)

exts= ('.jpg', '.JPG')
copyByExts(dataset_dir, target_dir, exts)
'''
