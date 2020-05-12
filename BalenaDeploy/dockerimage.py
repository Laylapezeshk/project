__author__ = 'Layla Pezeshkmehr, March 2020'

import os
import re
import sys
import json
import docker 
import datetime
import argparse
import subprocess
from crontab import CronTab
from balena import Balena
from operator import itemgetter


_repo_name = 'project/docker-edge1'
_tag = 'arm-latest'
_device_name = 'cold-breeze'
_app_name = 'Edge1CI'
_owner = 'lpezeshkmehr'
_owner_app_name = _owner + '/' + _app_name 
_app_file = 'app_spec.json'
_last_label_pushed = 'label.txt'

def get_device_uuid(_device_name, _app_file):
	with open (_app_file) as f:
		device_data = json.load(f)
	device_uuid = device_data[_device_name]
	return(device_uuid)


def docker_image(_repo_name, _tag):
	image_name = _repo_name + ':' + _tag
	client = docker.from_env()
	client.login(docker_username, docker_password)
	latest_image_pulled = client.images.pull(image_name)
	cmd_copy = 'docker inspect -f "{{json .Config.Labels }}" ' + image_name + ' |json_pp'
	fl = os.popen(cmd_copy)
	label_portion = fl.read()
	print (' \nLabel portion extracted from payload is:', label_portion)
	label_dict_persentation = json.loads(label_portion)
	label_last_image_pulled = label_dict_persentation['git-sha']
	print (' \nValue of the git-sha- Label of the last image pulled from dockerhub is :', label_last_image_pulled)
	return image_name, label_last_image_pulled
	

def balena_deploy(_owner_app_name, image_name, _device_name, _app_file):
	credentials = {'username': balena_username, 'password': balena_password}
	deploy_cmd = 'balena deploy ' + _owner_app_name + ' ' + image_name 
	balena = Balena()
	balena.auth.login(**credentials)
	f_deploy = os.popen(deploy_cmd)
	deploy_output= f_deploy.read()
	print ('deploy output is :', deploy_output)
	result = re.search(r'Release:\s[a-f0-9]{40}', deploy_output)	
	if result == None:
		print('Not a valid deploy output')
		return False
	release_string = result.group()
	print ('release_string is :', release_string)
	release_id = release_string.split(' ')[1].strip()
	print ('release_id is :', release_id)
	device_uuid = get_device_uuid(_device_name, _app_file)
	print ('device_uuid is: ', device_uuid )

	push_unit = balena.models.device.set_to_release(device_uuid,release_id)
	print (push_unit)
	if (push_unit is False):
		return False
	
	return True
	

def main():
	image_name, label_last_image_pulled = docker_image(_repo_name, _tag)
	print(' \nIn the def main() the label passed from docker_image def is: ', label_last_image_pulled)
	with open (_last_label_pushed, 'r+') as f_last_pushed:
		f_last_pushed_content = f_last_pushed.readline()
		print(' \nLabel inside the file indicates the last image pushed to the local device is: ',f_last_pushed_content, end='')
		if f_last_pushed_content != label_last_image_pulled:
			deploy = balena_deploy(_owner_app_name, image_name, _device_name, _app_file)

			if (deploy):
				f_last_pushed.seek(0)
				f_last_pushed.write(label_last_image_pulled)
			else:
				print(' \nBalena Deployment was unsuccessful')
		else:
			print(' \nLocal device is up to date, no new images since last image:', label_last_image_pulled)
	

if __name__== "__main__":

	parser = argparse.ArgumentParser()
	parser.add_argument('-ud','--usernamed',type = str, required = True,
			            help = 'You need to put the dockerhub username here')
	parser.add_argument('-pd','--passwordd', type = str, required = True,
			            help = 'you need to put the dockerhub password here')
	parser.add_argument('-ub','--usernameb',type = str, required = True,
			            help = 'You need to put the balena username here')
	parser.add_argument('-pb','--passwordb', type = str, required = True,
			            help = 'you need to put the balena password here')
	args = parser.parse_args()
	docker_username = args.usernamed
	docker_password = args.passwordd
	balena_username = args.usernameb 
	balena_password = args.passwordb
	
	main()
