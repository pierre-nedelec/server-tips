# Server & Terminal tips
  * [Server tips](#server-tips)
    + [Connection](#connection)
      - [Local desktop to remote](#local-desktop-to-remote)
      - [Tunnels](#tunnels)
      - [Intra server connection](#intra-server-connection)
    + [VS Code](#vs-code)
    + [Collaborating on the servers](#collaborating-on-the-servers)
      - [R packages](#r-packages)
    + [Install zsh without root access](#install-zsh-without-root-access)
      - [Install](#install)
      - [Configuration](#configuration)
  * [Terminal tips](#terminal-tips)
    + [ZSH](#zsh)
      - [Installation](#installation)
      - [Oh-My-Zsh](#oh-my-zsh)
      - [p10k](#p10k)
  * [Containers](#containers)
    + [Docker](#docker)
      - [DockerHub](#dockerhub)
    + [VS Code and Docker](#vs-code-and-docker)
    + [Singularity and Docker](#singularity-and-docker)
  * [Git](#git)
 
## Server tips

### Connection
#### Local desktop to remote
Set up SSH keys and configure your local computer to easily access servers!
* Create SSH keys:  
  An example to connect to Wynton ([source](https://wynton.ucsf.edu/hpc/howto/log-in-without-pwd.html))
  ```sh
  # Run the following lines in a terminal
  cd ~/.ssh
  ssh-keygen -f laptop_to_wynton
  ssh-copy-id -i ~/.ssh/laptop_to_wynton.pub USERNAME@log2.wynton.ucsf.edu
  ```
* Create or modify the file `~/.ssh/config` (see [sample file](local_ssh_config)).  
  Example:
  ```
  Host *.wynton.ucsf.edu
    User USERNAME
    IdentityFile ~/.ssh/laptop_to_wynton
  ```
* Then, simply connect via `ssh your_server`, without username or password!  
  Example: `ssh log2.wynton.ucsf.edu`


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


#### Intra server connection
If you need to connect from one remote computer to another on the same server (sharing `$HOME`), do the following from the login host:
```sh
# Create a ssh key-pair if not already existing (e.g. `id_rsa`)
ssh-keygen -t rsa

# Add the login host to authorized_hosts where dev1 is one of the host you'd like to connect to.
cat .ssh/id_rsa.pub | ssh dev1 'cat >> .ssh/authorized_keys'
```
There is no need to repeat the same operation for any other hosts!

### VS Code
[Visual Studio Code](https://code.visualstudio.com/) is a free code editor. It is pretty simple to start using it and it works great with ssh servers.

Once the ssh keys are in place, vscode can seamlessly connect to the server, and edit code as if it was on your local machine.
1. Download [VS Code](https://code.visualstudio.com/download)
2. In the left side bar, under 'Extensions', install the [SSH Extension](vscode:extension/ms-vscode-remote.remote-ssh). More info [here](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-ssh).
3. Once installed, click on the extension (in the left bar), and choose the host. It will prompt you for the ssh key asociated with it the first time.
4. Once in the server, click on 'Open folder...' to choose which folder to open!

NB: for #3, if your host default terminal is not bash, it can lead to errors when VS Code is trying to connect. To solve that, open the settings (UI), search for `remote.SSH.remotePlatform` and add your host name with `linux` as value. Save, and retry connecting to the host.


### Collaborating on the servers
#### R packages
To use a single collection of R packages shared across users, save the packages to a location accessible to all (e.g. `/group/R_libraries`). Then, create `~/.Renviron` in your home directory.
```
# .Renviron
# Define shared R library path at the user level
R_LIBS_USER = /group/R_libraries
```
Check that it worked by running `.libPaths()` in a R terminal. New packages will be installed there by default.


### Install zsh without root access
#### Install
The steps are highlighted in [zsh_install.sh](zsh_install.sh). This solution is inspired by [this article](https://www.drewsilcock.co.uk/compiling-zsh).

#### Configuration
To start zsh automatically, add the following to your `~/.bash_profile`:
```sh
export SHELL=$HOME/.local/bin/zsh #/usr/bin/zsh
exec $SHELL -l
```
For p10k configuration, see [p10k](#p10k)

On some servers, it is not recommended to perform the `exec` above (start a new shell from the `.bash_profile`). To circumvent that, create a `~/.start_zsh` file with these two lines in it and run it manually after the connection has been opened.

#### Use this install as default terminal in VS Code

In your host settings ("Preferences: Open Remote Settings (JSON) (SSH: pdev1)", or `workbench.action.openRemoteSettingsFile`), add the following lines:
```json
  "terminal.integrated.profiles.linux": {
    "zsh": {
      "path": "/wynton/protected/home/ci2/pnedelec/.start_zsh",
      "icon": "terminal-linux"
    },
    "bash": {
      "path": "bash",
      "icon": "terminal-bash",
      "args": ["-l"]
    }
  }
```

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

## Git

```sh
# Connect to repo:
git remote add origin git@git.ucsf.edu:path/to/repo
# Ensure ssh keys are activated
ssh -vT git@hostname.  # e.g. git.ucsf.edu
                       # if it returns an error, problem with ssh key
                       # if a key already exists, then it must be in the ssh-agent
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/your_private_key
```
