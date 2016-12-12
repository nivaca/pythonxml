#!/usr/bin/env bash
if test -e "venv.linux"; then
    echo "Currently: Mac environment setup."
    read -p "Do you wish to switch to LINUX setup? " answer
 if echo "$answer" | grep -iq "^y" ;then
        echo "Switching to Linux setup..."
        mv venv/ venv.mac/
        mv venv.linux/ venv/
        mv .idea/ .idea.mac/
        mv .idea.linux/ .idea/
    else
        echo "Aborted."
        exit 1
    fi
    exit 1
fi

if test -e "venv.mac"; then
    echo "Currently: Linux environment setup."
    read -p "Do you wish to switch to MAC setup? " answer
 if echo "$answer" | grep -iq "^y" ;then
        echo "Switching to Mac setup..."
        mv venv/ venv.linux/
        mv venv.mac/ venv/
        mv .idea/ .idea.linux/
        mv .idea.mac/ .idea/
    else
        echo "Aborted."
        exit 1
    fi
    exit 1
fi
