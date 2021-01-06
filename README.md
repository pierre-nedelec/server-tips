# A journey through UCSF

I joined UCSF in 2020, as part as a research lab in the Radiology and Biomedical Imaging department, focusing on brain research.

Here are some server/ML tips I gathered along the way.

## Terminal tips

### ZSH
#### Installation
zsh is installed by default on many computers. Try typing `zsh` in the terminal, and it should launch it.  
For details on how to install zsh without root access (for example on a server), see [Install zsh without root access](#Install-zsh-without-root-access)
#### Oh-My-Zsh
The installation is simple, once zsh is installed:
```sh
curl -L http://install.ohmyz.sh | sh
```
#### p10k
```sh
git clone --depth=1 https://github.com/romkatv/powerlevel10k.git ${ZSH_CUSTOM:-$HOME/.oh-my-zsh/custom}/themes/powerlevel10k\n
```
The next time zsh is started, the command prompt will ask you to configure p10k interactively. If you want to reuse a previously made configuration, replace the `.p10k.zsh` file in your home directory, after running the configuration wizzard once.

## Server use

### Connection
#### Local desktop to remote
Set up SSH keys and configure your local computer to easily access servers!
* SSH keys: https://wynton.ucsf.edu/hpc/howto/log-in-without-pwd.html
* Computer setup: `~/.ssh/config`, see [sample file](local_ssh_config).
Then, simply connect via `ssh your_server`, without username or password!

#### Intra server connection
If you need to connect from one remote computer to another on the same server (sharing `$HOME`), do the following from the login host:
```sh
# Create a ssh key-pair if not already existing (e.g. `id_rsa`)
ssh-keygen -t rsa

# Add the login host to authorized_hosts where dev1 is one of the host you'd like to connect to.
cat .ssh/id_rsa.pub | ssh dev1 'cat >> .ssh/authorized_keys'
```
There is no need to repeat the same operation for any other hosts!

#### Tunnels
If one server is only accessible after connecting to a login node, add a tunnel to your `.ssh/config` [file](local_ssh_config):
```
Host dev_server
  HostName dev_server_ip
  ProxyJump login.server.ip
  IdentityFile ~/.ssh/laptop_to_loginnode
  User USER
```
This will also allow the use of `vscode` or other software. Then the remote server is accessible seemlessly from your local computer with `ssh dev_server`.

### Collaborating on the servers
#### R packages
To use a single collection of R packages shared across users, save the packages to a location accessible to all (e.g. `/group/R_libraries`). Then, create `~/.Renviron` in your home directory.
```
# .Renviron
# Define shared R library path at the user level
R_LIBS_USER = /group/R_libraries
```
Check that it worked by running `.libPaths()` in a R terminal.


### Install zsh without root access
#### Install
The steps are highlighted in [zsh_install.sh](zsh_install.sh). This solution is inspired by [this article](https://www.drewsilcock.co.uk/compiling-zsh).

#### Configuration
To start zsh automatically, add the following to your `~/.bash_profile`, or if it exists `~/.bashrc`:
```sh
export SHELL=$HOME/.local/bin/zsh #/usr/bin/zsh
exec $SHELL -l
```
For p10k configuration, see [p10k](#p10k)


## Containers
### Docker
#### DockerHub
* Create a repo, e.g. named `my_repo`
* Create an access token ([Settings](https://hub.docker.com/settings/security))
* Login from the command line with `docker login --username my_username`, using the access code given above
* Get image ID of the Docker image to upload: `docker images`
* Tag the image to upload like so: `docker tag my_image_id my_username/my_repo:my_tag` where `my_tag` is a custom tag (e.g. 0.1, 1.0, 2.2, ...)
* Check it was correctly created by running `docker images` again
* Upload image to server with `docker push my_username/my_repo:my_tag`. It should output:
```
The push refers to repository [docker.io/my_username/my_repo]
keylsdn45l4e5: Preparing
...
```

### VS Code and Docker
### Singularity and Docker
