# vim

## 配置说明

1. 下载完之后，将 .vimrc .bashrc tools 拷贝到自己的用户目录下
2. 将 vim.tar.* 解压成得到 .vim 文件夹，拷贝到自己的用户目录下
解压命令：cat vim.tar.bz2.a* | tar xj
3. 将.vimrc .bashrc tools 中的配置找到 "/home/zhengxiasong" 替换成自己的用户目录
4. 执行source .bashrc, source .vimrc 即可生效

**注意如果之前自己已经有配置文件，请做好相应的备份**

## 把 \<leader> 设置成空格

let mapleader = "\<Space>"
let g:mapleader = "\<Space>"
文件和函数、单词搜索系列

## ctrlp

作用：模糊搜索文件
相关快捷键：

\<leade\>p ——搜索文件名

\<leader>o ——同时在文件，缓冲区和最近最多修改中搜索

\<leader>f  ——最近最多修改中搜索

esc——退出

更多的插件本身的快捷键功能可以输入:help ctrlp-mappings@cn进行查看

bu——打开已打开的缓冲文件列表，可以进行删除

tl——打开当前文件的变量和函数列表


## 打开多个窗口切换

ctrl+j ——切换到上一个窗口
ctrl+k ——切换到下一个窗口
ctrl+h ——切换左边的窗口
ctrl+l ——切换右边的窗口

*——在本文件中向后查找当前光标的单词

#——在本文件中向后查找当后光标的单词

输入一次之后，可使用 n 替换，shift+n则执行相反的查找
 
需要安装ctags+cscope

空格+s ——查找本项目中的包含光标所在单词的位置

F6——查看查找的列表

F3——向前查找
F4——向后查找

## 高亮标签系列
 
对当前文件行打标签
m+a-z——当前行打标签，并且会显示对应的a-z

'+a-z——跳转到对应行标签
F7——显示行标签列表
F10——清除本文件所有的行标签 

\<leader>+m——高亮或者取消高亮当前光标的单词，可以不同的单词，打标签的颜色不一样

\<leader>+/ ——查找当前文件的高亮的单词位置

## airline

bn ——切换到下一个标签页

bp ——切换到上一个标签也

\<leader>b ——显示所有的标签也列表等待切换

## undo

F5 ——打开undo界面，可以进行回滚

## tagbar

tb ——打开tagbar界面
