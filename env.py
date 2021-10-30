import os
from dotenv import dotenv_values

var = {
  **dotenv_values(".env"),
  **dotenv_values(".env.local"),
  **os.environ
}

def get(key):
  return var[key]