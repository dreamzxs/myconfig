# ~/.bashrc: executed by bash(1) for non-login shells.
# see /usr/share/doc/bash/examples/startup-files (in the package bash-doc)
# for examples

# If not running interactively, don't do anything
[ -z "$PS1" ] && return

# don't put duplicate lines in the history. See bash(1) for more options
# ... or force ignoredups and ignorespace
HISTCONTROL=ignoredups:ignorespace

# append to the history file, don't overwrite it
shopt -s histappend

# for setting history length see HISTSIZE and HISTFILESIZE in bash(1)
HISTSIZE=1000
HISTFILESIZE=2000

# check the window size after each command and, if necessary,
# update the values of LINES and COLUMNS.
shopt -s checkwinsize

# make less more friendly for non-text input files, see lesspipe(1)
[ -x /usr/bin/lesspipe ] && eval "$(SHELL=/bin/sh lesspipe)"

# set variable identifying the chroot you work in (used in the prompt below)
if [ -z "$debian_chroot" ] && [ -r /etc/debian_chroot ]; then
    debian_chroot=$(cat /etc/debian_chroot)
fi

# set a fancy prompt (non-color, unless we know we "want" color)
case "$TERM" in
    xterm-color) color_prompt=yes;;
esac

# uncomment for a colored prompt, if the terminal has the capability; turned
# off by default to not distract the user: the focus in a terminal window
# should be on the output of commands, not on the prompt
force_color_prompt=yes

if [ -n "$force_color_prompt" ]; then
    if [ -x /usr/bin/tput ] && tput setaf 1 >&/dev/null; then
	# We have color support; assume it's compliant with Ecma-48
	# (ISO/IEC-6429). (Lack of such support is extremely rare, and such
	# a case would tend to support setf rather than setaf.)
	color_prompt=yes
    else
	color_prompt=
    fi
fi

find_git_branch () {
    local dir=. head
    until [ "$dir" -ef / ]; do
        if [ -f "$dir/.git/HEAD" ]; then
            head=$(< "$dir/.git/HEAD")
            if [[ $head = ref:\ refs/heads/* ]]; then
                git_branch="(${head#*/*/})"
            elif [[ $head != '' ]]; then
                git_branch="(detached)"
            else
                git_branch="(unknow)"
            fi
            return
        fi
        dir="../$dir"
    done
    git_branch=''
}

PROMPT_COMMAND="find_git_branch; $PROMPT_COMMAND"

if [ "$color_prompt" = yes ]; then
    PS1='${debian_chroot:+($debian_chroot)}\[\033[01;32m\]\u@\h\[\033[31;35;1m\]$git_branch\[\033[00m\]\[\033[00m\]:\[\033[01;36m\]\w\[\033[32m\]\$\n\[\033[00m\]'
    #PS1='${debian_chroot:+($debian_chroot)}\[\033[01;32m\]\u@\h\[\033[00m\]:\[\033[01;36m\]\W\[\033[32m\]\$\[\033[00m\] '
else
    PS1='${debian_chroot:+($debian_chroot)}\u@\h:\W\$\n'
fi
unset color_prompt force_color_prompt

# If this is an xterm set the title to user@host:dir
case "$TERM" in
xterm*|rxvt*)
    PS1="\[\e]0;${debian_chroot:+($debian_chroot)}\u@\h: \w\a\]$PS1"
    ;;
*)
    ;;
esac

# enable color support of ls and also add handy aliases
if [ -x /usr/bin/dircolors ]; then
    test -r ~/.dircolors && eval "$(dircolors -b ~/.dircolors)" || eval "$(dircolors -b)"
    alias ls='ls --color=auto'
    #alias dir='dir --color=auto'
    #alias vdir='vdir --color=auto'

    alias grep='grep --color=auto'
    alias fgrep='fgrep --color=auto'
    alias egrep='egrep --color=auto'
    alias buildtags='~/tools/buildtags.sh'
    alias lookupfile='~/tools/lookfile.sh'
fi

# some more ls aliases
alias ll='ls -alF'
alias la='ls -A'
alias l='ls -CF'

# some more find aliases
alias zfind='find . -name'

alias j='autojump'

alias v='nvim'

# some more cd aliases
alias ..='cd ..'
alias ...='cd ../..'
alias ....='cd ../../..'
alias .....='cd ../../../..'
alias cd2='cd ..'
alias cd3='cd ../..'
alias cd4='cd ../../..'
alias cd5='cd ../../../..'
alias cdkernel='cd ~/code/cros/src/third_party/kernel/v4.4'
alias cdec='cd ~/code/cros/src/platform/ec'
alias cdcoreboot='cd ~/code/cros/src/third_party/coreboot'
alias cdoverlay='cd ~/code/cros/src/overlays'
alias cdimage='cd ~/code/cros/src/build/images'
alias cdproject='cd ~/code/cros'
alias cdchrome='cd ~/code/cros/src/chrome_root/src'
alias cddts='cd ~/code/cros/src/third_party/kernel/v4.4/arch/arm64/boot/dts/rockchip'

# some more source aliases
alias sourcevim='source ~/.vimrc'
alias sourcebashrc='source ~/.bashrc'

# Alias definitions.
# You may want to put all your additions into a separate file like
# ~/.bash_aliases, instead of adding them here directly.
# See /usr/share/doc/bash-doc/examples in the bash-doc package.

if [ -f ~/.bash_aliases ]; then
    . ~/.bash_aliases
fi

# enable programmable completion features (you don't need to enable
# this, if it's already enabled in /etc/bash.bashrc and /etc/profile
# sources /etc/bash.bashrc).
if [ -f /etc/bash_completion ] && ! shopt -oq posix; then
    . /etc/bash_completion
fi

alias rd='pushd $PWD'
alias ld='dirs -v'
alias gd='pushd'
function col()
{
    awk -v num=$1 '{print $num}'
}
function cdx()
{
    local g_cur_path=`pwd|tr '/' ' '`
    local my_path=""
    for i in $g_cur_path
    do
        my_path=$my_path/$i
        if [[ ${i/${1}//} != $i ]];then
                cd $my_path
                break;
        fi
    done
}
#luojie add --end

######################## dir func ################
DIR_LIST=~/.dir_list
function cdsave()
{
    echo $PWD>>$DIR_LIST
    echo "Save current path: $PWD"
}
function cdlist()
{
    if [ -f $DIR_LIST  ];then
        cat -n $DIR_LIST
    fi
}
function cdclear()
{
    echo -e "\c"> $DIR_LIST
}

function cdgo()
{
    if [ $# != 1 ];then
        echo "please select a number from dirlist"
        cdlist
    else
        line=`sed -n "$1p" $DIR_LIST`
        cd $line
    fi
}
######################## end #################

#export
export PYTHONSTARTUP=~/.pystartup
alias tmux='TERM=screen-256color tmux'
