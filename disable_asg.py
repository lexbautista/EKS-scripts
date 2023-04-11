import subprocess
import argparse
import json
import sys


### Add arg parser for nodegroups and region
parser = argparse.ArgumentParser()
parser.add_argument('-r', '--region', action='store', dest='region', help='Set region')
parser.add_argument('-n', '--nodegroups', action='store', dest='nodegroups', help='Set nodegroups')
parser.add_argument('-c', '--cluster', action='store', dest='cluster', help='Set nodegroups')
args = parser.parse_args()

nodegroups = args.nodegroups
region = args.region
cluster = args.cluster

### Turns string of nodegroups into list
def create_nodegroup_list():
    remove_bracket = nodegroups.replace("[", "").replace("]","").replace(" ", "")
    nodegroup_list = remove_bracket.split(",")
    return(nodegroup_list)

### Parse ASG for ASG group name
def parse_asg_group_name():
    try:
        nodegroups = create_nodegroup_list()
        asg_name_list = []
        for ng in nodegroups:
            value = "eksctl-" + cluster + "-nodegroup-" + ng
            get_asg_name_command = "aws autoscaling describe-auto-scaling-groups --query 'AutoScalingGroups[?contains(Tags[?Key==`aws:cloudformation:stack-name`].Value, `" + value + "`)]' --region " + region + " --output json > asg.json"
            subprocess.check_output(get_asg_name_command, shell=True, encoding='utf-8')
            with open('asg.json', 'r') as f:
                data = json.load(f)
                for i in data:
                    asg_name_list.append(i["AutoScalingGroupName"])
        return(asg_name_list)
    except:
        sys.exit("ERROR: Unable to parse ASG JSON")


### Suspends process for ASGs
def disable_asg():
    asg_name_list = parse_asg_group_name()
    
    for asg in asg_name_list:
        disable_command = "aws autoscaling suspend-processes --region " + region + " --auto-scaling-group-name " + asg
        print(disable_command)
        subprocess.run(disable_command, shell=True, encoding='utf-8')
        resume_command = "aws autoscaling resume-processes --region " + region + " --auto-scaling-group-name " + asg + " --scaling-processes Terminate"
        print(resume_command)
        subprocess.run(resume_command, shell=True, encoding='utf-8')

### Resumes all processes for ASGs
def resume_asg():
    asg_name_list = parse_asg_group_name()
    
    for asg in asg_name_list:
        resume_command = "aws autoscaling resume-processes --region " + region + " --auto-scaling-group-name " + asg
        print(resume_command)
        subprocess.run(resume_command, shell=True, encoding='utf-8')

disable_asg()
