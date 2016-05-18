"""ShutIt module. See http://shutit.tk
"""

from shutit_module import ShutItModule
import random
import string

class docker_101_tutorial(ShutItModule):

	def build(self, shutit):
		# Some useful API calls for reference. See shutit's docs for more info and options:
		#
		# ISSUING BASH COMMANDS
		# shutit.send(send,expect=<default>) - Send a command, wait for expect (string or compiled regexp)
		#                                      to be seen before continuing. By default this is managed
		#                                      by ShutIt with shell prompts.
		# shutit.multisend(send,send_dict)   - Send a command, dict contains {expect1:response1,expect2:response2,...}
		# shutit.send_and_get_output(send)   - Returns the output of the sent command
		# shutit.send_and_match_output(send, matches)
		#                                    - Returns True if any lines in output match any of
		#                                      the regexp strings in the matches list
		# shutit.send_until(send,regexps)    - Send command over and over until one of the regexps seen in the output.
		# shutit.run_script(script)          - Run the passed-in string as a script
		# shutit.install(package)            - Install a package
		# shutit.remove(package)             - Remove a package
		# shutit.login(user='root', command='su -')
		#                                    - Log user in with given command, and set up prompt and expects.
		#                                      Use this if your env (or more specifically, prompt) changes at all,
		#                                      eg reboot, bash, ssh
		# shutit.logout(command='exit')      - Clean up from a login.
		#
		# COMMAND HELPER FUNCTIONS
		# shutit.add_to_bashrc(line)         - Add a line to bashrc
		# shutit.get_url(fname, locations)   - Get a file via url from locations specified in a list
		# shutit.get_ip_address()            - Returns the ip address of the target
		# shutit.command_available(command)  - Returns true if the command is available to run
		#
		# LOGGING AND DEBUG
		# shutit.log(msg,add_final_message=False) -
		#                                      Send a message to the log. add_final_message adds message to
		#                                      output at end of build
		# shutit.pause_point(msg='')         - Give control of the terminal to the user
		# shutit.step_through(msg='')        - Give control to the user and allow them to step through commands
		#
		# SENDING FILES/TEXT
		# shutit.send_file(path, contents)   - Send file to path on target with given contents as a string
		# shutit.send_host_file(path, hostfilepath)
		#                                    - Send file from host machine to path on the target
		# shutit.send_host_dir(path, hostfilepath)
		#                                    - Send directory and contents to path on the target
		# shutit.insert_text(text, fname, pattern)
		#                                    - Insert text into file fname after the first occurrence of
		#                                      regexp pattern.
		# shutit.delete_text(text, fname, pattern)
		#                                    - Delete text from file fname after the first occurrence of
		#                                      regexp pattern.
		# shutit.replace_text(text, fname, pattern)
		#                                    - Replace text from file fname after the first occurrence of
		#                                      regexp pattern.
		# ENVIRONMENT QUERYING
		# shutit.host_file_exists(filename, directory=False)
		#                                    - Returns True if file exists on host
		# shutit.file_exists(filename, directory=False)
		#                                    - Returns True if file exists on target
		# shutit.user_exists(user)           - Returns True if the user exists on the target
		# shutit.package_installed(package)  - Returns True if the package exists on the target
		# shutit.set_password(password, user='')
		#                                    - Set password for a given user on target
		#
		# USER INTERACTION
		# shutit.get_input(msg,default,valid[],boolean?,ispass?)
		#                                    - Get input from user and return output
		# shutit.fail(msg)                   - Fail the program and exit with status 1
		#
		vagrant_image = shutit.cfg[self.module_id]['vagrant_image']
		vagrant_provider = shutit.cfg[self.module_id]['vagrant_provider']
		module_name = 'docker_101_tutorial_' + ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(6))
		shutit.send('rm -rf /tmp/' + module_name + ' && mkdir -p /tmp/' + module_name + ' && cd /tmp/' + module_name)
		shutit.send('vagrant init ' + vagrant_image)
		shutit.send('vagrant up --provider virtualbox',timeout=99999)
		shutit.login(command='vagrant ssh')
		shutit.login(command='sudo su -',password='vagrant')

		# DOCKER SETUP
		shutit.install('docker.io')
		shutit.send('cat /etc/issue',note='We are in an ubuntu vm')
		shutit.send('yum',check_exit=False,note='yum is not available, for example')

		# DOCKER RUN
		shutit.login('docker run -ti --name docker-101-centos centos /bin/bash',note='Run up a centos docker image and attach to it with the bash command.',timeout=999)
		shutit.install('iproute')
		shutit.send('ps -ef',note='We are in a container, only the bash process is running')
		shutit.send('ip route',note='We have our own network stack')
		shutit.send('whoami',note='By default I am root')
		shutit.send('ls',note='And we have our own filesystem')
		shutit.logout(note='log out of the bash shell, terminating the container - type exit')

		# DOCKER PS
		shutit.send('docker ps -a',note='That container is still there, but not running because the bash process terminated when we logged out.')

		# DOCKER RM
		shutit.send('docker rm docker-101-centos',note='Remove the container.')
		shutit.send('docker ps -a',note='The container has gone.')
		shutit.send('echo',note='Next we start up 100 containers.')
		for i in range(1,100):
			shutit.send('docker run -d --name centos_container_' + str(i) + ' centos sleep infinity',timeout=500)

		shutit.send('docker ps',note='Show all 100 containers.')

		# DOCKER EXEC
		shutit.login(command='docker exec -ti centos_container_1 /bin/bash',note='Log onto container 1 to create a file that only exists in that container')
		shutit.send('pwd',note='We start in the root folder.')
		shutit.send('touch myfile',note='Create file: myfile.')
		shutit.send('ls',note='The file is there.')
		shutit.logout(note='log out of the bash shell - type exit')

		shutit.login('docker exec -ti centos_container_2 /bin/bash',note='Log onto container 2 to show the file is not there.')
		shutit.send('pwd',note='We start in the root folder here too.')
		shutit.send('ls',note='The file "myfile" is not here.')
		shutit.logout(note='log out of the bash shell - type exit')

		shutit.login(command='docker exec -ti centos_container_1 /bin/bash',note='Log onto container 1 again')
		shutit.send('ls',note='The file "myfile" is still there in the first container.')
		shutit.logout(note='log out of the bash shell - type exit')

		# DOCKER IMAGES
		shutit.send('docker images',note='We can list the images we have on this _host_. We have one image (the centos one) which is the source of all our containers.')
		shutit.send('docker ps',note='But we have 100 containers.')

		# DOCKER COMMIT / HISTORY / LAYERS
		shutit.send('docker history centos',note='Containers are composed of _layers_. Each one represents a set of file changes analagous (but not the same as) a git commit. This is the history of the "centos" image layers.')
		shutit.send('docker commit centos_container_1 docker_101_image',note='To create a new image with myfile in, commit the container.')
		shutit.send('docker ps -q -a | xargs -n 1 docker rm -f 2>&1 > /dev/null &',note='Delete all containers in the background.')
		shutit.send('docker images',note='That image is now listed alongside the centos one on our host.')
		shutit.send('docker history centos',note='Show the centos history.')
		shutit.send('docker history docker_101_image',note='Show the docker_101_image history. It is the same as the centos image with our extra layer.')

		# DOCKER LOGIN
		shutit.pause_point('Now log in to docker with "docker login" please.')
		docker_username = shutit.get_input('Please input your dockerhub username: ')
		shutit.send('docker tag docker_101_image ' + docker_username + '/docker_101_image',note='Re-tag the image with your docker username-space.')
		shutit.send('docker images',note='It is listed as a separate image with the same ID.')
		shutit.send('docker push ' + docker_username + '/docker_101_image',note='It is listed as a separate image with the same ID.')

		# PULL
		shutit.send('docker rmi ' + docker_username + '/docker_101_image',note='Delete our newly-created image.')
		shutit.send('docker rmi docker_101_image',note='Delete the previously-created identical image also.')
		shutit.send('docker images',note='Neither image is now available. Only the centos image remains, which we keep to avoid re-downloading.')
		shutit.send('docker pull ' + docker_username + '/docker_101_image',note='Pull the image back down. Notice it is a lot faster as only the extra layer we created is required.')
		shutit.login('docker run -ti ' + docker_username + '/docker_101_image /bin/bash',note='Run up bash in a new container from that image.')
		shutit.send('pwd',note='I am in the root folder again')
		shutit.send('ls',note='And the file we create earlier is there')
		shutit.logout(note='exit the container')
		shutit.send('docker ps -a -q | xargs docker rm -f',note='Clean up all containers on the host.')
		shutit.send('docker rmi ' + docker_username + '/docker_101_image',note='Remove the image we just pulled.')

		# DOCKERFILE
		shutit.send('mkdir -p docker_build && cd docker_build',note='Create a folder for our build.')
		shutit.send('''cat > Dockerfile << END
FROM centos
RUN touch /root/myfile
CMD ['/bin/bash']
END''')
		shutit.send('cat Dockerfile',note='Cat the Dockerfile created for you. This Dockerfile that does the same action as before.')
		docker_image_name = shutit.get_input('Please input a new image name.')
		shutit.send('docker build -t ' + docker_username + '/' + docker_image_name + ' .',note='Build the docker image using the Dockerfile (rather than running and committing), and tag it with a new image name')
		shutit.send('docker push ' + docker_username + '/' + docker_image_name,note='Push the image to the dockerhub')
		shutit.send('docker rmi ' + docker_username + '/' + docker_image_name,note='Remove the image from our local machine')
		shutit.send('docker images',note='It is no longer available. Only the centos image remains.')
		shutit.send('rm -rf Dockerfile',note='Remove the Dockerfile we created')

		# DOCKERFILE FROM THAT BASE
		shutit.send('''cat > Dockerfile << END
FROM ''' + docker_username + '/' + docker_image_name + '''
RUN touch /root/myfile2
CMD ['/bin/bash']
END''')
		shutit.send('cat Dockerfile',note='Dockerfile created for you that builds on the last one (rather than centos).')
		shutit.send('docker build -t newimage .',note='Build this new image from the new Dockerfile.')
		shutit.login('docker run -ti newimage /bin/bash',note='Run the newly-create image.')
		shutit.send('ls',note='The file myfile2 (from our new layer) and myfile (from our old image) is there.')
		shutit.logout(note='Log out of the new container - type exit')
		shutit.send('docker rmi newimage',note='Destroy this new image')
		shutit.send('docker ps -a -q | xargs docker rm -f',note='Clean up all containers on the host.')

		shutit.logout()
		shutit.logout()
		return True

	def get_config(self, shutit):
		# CONFIGURATION
		# shutit.get_config(module_id,option,default=None,boolean=False)
		#                                    - Get configuration value, boolean indicates whether the item is
		#                                      a boolean type, eg get the config with:
		# shutit.get_config(self.module_id, 'myconfig', default='a value')
		#                                      and reference in your code with:
		# shutit.cfg[self.module_id]['myconfig']
		shutit.get_config(self.module_id,'vagrant_image',default='ubuntu/trusty64')
		shutit.get_config(self.module_id,'vagrant_provider',default='virtualbox')
		return True

def module():
	return docker_101_tutorial(
		'tk.shutit.docker_101_tutorial', 1845506479.0001123,
		description='',
		maintainer='',
		delivery_methods=['bash'],
		depends=['shutit.tk.setup','shutit-library.virtualbox.virtualbox.virtualbox','tk.shutit.vagrant.vagrant.vagrant']
	)
