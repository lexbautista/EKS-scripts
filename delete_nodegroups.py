import subprocess
import argparse

### Add arg parser for nodegroup
parser = argparse.ArgumentParser()
parser.add_argument('-r', '--region', action='store', dest='region', help='Set region')
parser.add_argument('-c', '--cluster', action='store', dest='cluster', help='Set cluster')
parser.add_argument('-n', '--nodegroups', action='store', dest='nodegroups', help='Set nodegroups')
args = parser.parse_args()

nodegroups = args.nodegroups
cluster = args.cluster
region = args.region

### Turns string of nodegroups into list
def create_nodegroup_list():
    remove_bracket = nodegroups.replace("[", "").replace("]","").replace(" ", "")
    nodegroup_list = remove_bracket.split(",")
    return(nodegroup_list)

### Deletes old nodegroups
def delete_nodegroups():
    nodegroups = create_nodegroup_list()
    for ng in nodegroups:
        command = "eksctl delete nodegroup --cluster=" + cluster +  " --name=" + ng + "--region=" + region
        subprocess.run(command, shell=True, encoding='utf-8')

    
delete_nodegroups()

