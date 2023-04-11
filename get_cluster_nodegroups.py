import subprocess
import json
import argparse

### Add arg parser for nodegroup file and region
parser = argparse.ArgumentParser()
parser.add_argument('-c', '--cluster', action='store', dest='cluster', help='Set cluster')
parser.add_argument('-r', '--region', action='store', dest='region', help='Set region')
args = parser.parse_args()
cluster = args.cluster
region = args.region

### Get nodegroups from the cluster and output to json file
def get_all_nodegroups():
    command = "eksctl get nodegroups --cluster " + cluster + " --region " + region + " --output json > cluster.json"
    subprocess.run(command, shell=True, encoding='utf-8')

### Parse json file and get nodegroup names
def all_nodegroup_list():
    get_all_nodegroups()

    nodegroup_list = []
    with open('cluster.json', 'r') as f:
        data = json.load(f)
    for name in data:
        nodegroup_list.append(name["Name"])
    print(nodegroup_list)

all_nodegroup_list()
