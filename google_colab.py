"""
    Some of the colab snippets I use on a daily basis.
    I've decided to store those as .py for faster access from github and easier imports.
"""
"""
    Zips a folder and downloads it. Can also copy the archive to a google drive path (or any other available to your colab instance)
    Use to automatically download results after some afk training or inference, before the instance resets.

    path: path to a folder to download. Can contain wildcards
    prefix: a name of your new archive
    drive: a folder to copy the archive to
"""
from google.colab import files
import time

def download(path, prefix, drive=''):
  print('\nCкачиваем...\n')
  timestamp = round(time.time())
  !zip -r /content/{prefix}-{timestamp}.zip {path}
  files.download(f"/content/{prefix}-{timestamp}.zip")
  if drive!='':
      !cp "/content/{prefix}-{timestamp}.zip" {drive}


"""
    It beeps. Use to give yourself a signal.
"""
from google.colab import output
def beep():
  output.eval_js('new Audio("https://upload.wikimedia.org/wikipedia/commons/0/05/Beep-09.ogg").play()')
