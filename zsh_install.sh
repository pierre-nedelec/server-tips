#!/usr/bin/bash
cd ~/utils

# Download the ncurses gzipped tarball
wget ftp://ftp.invisible-island.net/ncurses/ncurses.tar.gz

# Extract gzipped tarball
tar -zxvf ncurses.tar.gz

# Move into root ncurses source directory
cd ncurses

# Set cflags and c++ flags to compile with Position Independent Code enabled
export CXXFLAGS=' -fPIC'
export CFLAGS=' -fPIC'

# Produce Makefile and config.h via config.status
./configure --prefix=$HOME/.local --enable-shared

# Compile (takes a while)
make

# Deduce environment information and build private terminfo tree
cd progs
./capconvert
cd ..

# Test compile
./test/ncurses

# Install ncurses to $HOME/.local
make install


INSTALL_PATH='$HOME/.local'

export PATH=$INSTALL_PATH/bin:$PATH
export LD_LIBRARY_PATH=$INSTALL_PATH/lib:$LD_LIBRARY_PATH
export CFLAGS=-I$INSTALL_PATH/include
export CPPFLAGS="-I$INSTALL_PATH/include" LDFLAGS="-L$INSTALL_PATH/lib"

### Install ZSH
cd ~/utils
# Clone zsh repository from git
git clone git://github.com/zsh-users/zsh.git

# Move into root zsh source directory
cd zsh

# Produce config.h.in, needed to produce config.status from ./configure
autoheader

# Produce the configure file from aclocal.m4 and configure.ac
autoconf

# Give autotools a timestamp for recompilation
date > stamp-h.in  ## added by Pierre
date < stamp-h.in

# Produce Makefile and config.h via config.status
./configure --prefix=$HOME/.local --enable-shared

# Compile
make

# Install
make install


### Install Oh-My-ZSH
curl -L http://install.ohmyz.sh | sh

