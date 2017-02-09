#!/bin/bash
#初期設定
git config --global user.name "First-name Family-name"
git config --global user.email "username@example.com"
#nano からVimへ
git config --global core.editor 'vim -c "set fenc=utf-8"'
#git diff に色付け
git config --global color.diff auto
git config --global color.status auto
git config --global color.branch auto

