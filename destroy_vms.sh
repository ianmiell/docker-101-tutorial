#!/bin/bash
#set -x
if [[ $(which VBoxManage) != '' ]]
then
while true 
do
	VBoxManage list runningvms | grep docker_101_tutorial | awk '{print $1}' | xargs -IXXX VBoxManage controlvm 'XXX' poweroff && VBoxManage list vms | grep docker_101_tutorial | awk '{print $1}'  | xargs -IXXX VBoxManage unregistervm 'XXX' --delete
	if [[ $(VBoxManage list vms | grep docker_101_tutorial | wc -l) -eq '0' ]]
	then
		break
	else
		ps -ef | grep virtualbox | grep docker_101_tutorial | awk '{print $2}' | xargs kill
		sleep 10
	fi
done
fi
