#!/bin/bash
bash ./destroy_vms.sh
[[ -z "$SHUTIT" ]] && SHUTIT="$1/shutit"
[[ ! -a "$SHUTIT" ]] || [[ -z "$SHUTIT" ]] && SHUTIT="$(which shutit)"
if [[ ! -a "$SHUTIT" ]]
then
	echo "Must have shutit on path, eg export PATH=$PATH:/path/to/shutit_dir"
	exit 1
fi
$SHUTIT build -d bash -m shutit-library/vagrant:shutit-library/virtualbox "$@" --training
if [[ $? != 0 ]]
then
	exit 1
fi
