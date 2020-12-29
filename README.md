# A journey through UCSF

I joined UCSF in 2020, as part as a research lab in the Radiology and Biomedical Imaging department, focusing on brain research.

Here are some server/ML tips I gathered along the way.

## Terminal tips

### ZSH

### Oh-My-Zsh and p10k

## Server use

### Connection
Set up SSH keys and configure your local computer to easily access servers!
* SSH keys: https://wynton.ucsf.edu/hpc/howto/log-in-without-pwd.html
* Computer setup: `~/.ssh/config`, see [sample file](local_ssh_config).
Then, simply connect via `ssh your_server`, without username or password!

### Install zsh without root access


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
