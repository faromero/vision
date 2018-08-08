import sys
import os
import torch
import shutil

class PyCache(object):

  def __init__(self, model, dir=os.getcwd()):
    self._dir = os.path.join(dir, ".pycache")
    self._model = model

    if os.path.isdir(self._dir):
      print("Cache directory already exists at", self._dir)
    else:
      print("Cache directory does not yet exist, creating...")
      os.mkdir(self._dir)

  def search(self, query):
    content = None
    curr_dir = os.path.join(self._dir, self._model)
    if os.path.isdir(curr_dir):
      next_hash = str(abs(torch.sum(query).data.tolist()))
      curr_file = os.path.join(curr_dir, next_hash)
      if os.path.isfile(curr_file):
        content = torch.load(curr_file)

    return content

  def insert(self, query, content):
    curr_dir = os.path.join(self._dir, self._model)
    if not os.path.isdir(curr_dir):
      os.mkdir(curr_dir)

    next_hash = str(abs(torch.sum(query).data.tolist()))
    curr_file = os.path.join(curr_dir, next_hash)
    torch.save(content, curr_file)

  def clear(self):
    shutil.rmtree(self._dir)
    print("Cache successfully cleared")


