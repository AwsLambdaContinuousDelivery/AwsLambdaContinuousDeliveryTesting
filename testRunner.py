import os, sys, boto3
import argparse
import subprocess
import yaml

from typing import List

def getTests(path: str) -> List[str]:
  files = os.listdir(path)
  files = map(lambda x: "/".join([path, x]), files)
  files = filter(lambda x: x.endswith(".py"), files)
  return list(files)

def loadConfig(path: str) -> dict:
  config = {}
  with open (path + "/config/config.yaml", "r") as c:
    config = yaml.load(c)
  if not config:
    raise Exception("Empty config")
  return config

def getArn(path: str, stack: str, stage: str) -> str:
  config = loadConfig(path)
  funcName = config["Name"] + stack + stage
  client = boto3.client('cloudformation')
  res = client.list_exports()
  while res is not None:
    for export in res["Exports"]:
      if export["Name"] == funcName:
        return export["Value"]
    if "NextToken" not in res:
      res = None
    else:
      res = client.list_exports(NextToken = res["NextToken"])
  raise Exception("No ARN found for " + funcName)

def exec_tests(path: str, stack: str, stage: str):
  arn = getArn(path, stack, stage)
  tests = getTests(path + "/test")
  for test_file in tests:
    exec_cmd = " ".join(["python3", test_file, arn])
    result = subprocess.check_output(exec_cmd, shell=True)
    print(result)
  return 0

if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument("-p", "--path", help="Path of the folder with the source \
                       -code of the aws lambda functions", type = str, required = True)
  parser.add_argument("--stack", help="StackName", type = str, required = True)
  parser.add_argument("--stage", help="Name of the stage", type = str, required = True)
  args = parser.parse_args()
  exec_tests(args.path, args.stack, args.stage)