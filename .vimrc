set nocompatible              " be iMproved, required
filetype off                  " required
" set the runtime path to include Vundle and initialize
set rtp+=$HOME/.vim/bundle/Vundle.vim
call vundle#begin()
" alternatively, pass a path where Vundle should install plugins
"call vundle#begin('~/some/path/here')

Plugin 'kshenoy/vim-signature'

" let Vundle manage Vundle, required
Plugin 'VundleVim/Vundle.vim'

"查看Git详细提交日志(类似gitk)
"Bundle "gregsexton/gitv"

"GitGutter 实时显示git更改
Bundle "airblade/vim-gitgutter"

"also can install git clone git://github.com/tpope/vim-fugitive.git
Bundle "tpope/vim-fugitive"

Bundle 'ctrlpvim/ctrlp.vim'

Bundle 'tacahiroy/ctrlp-funky'

Bundle 'sheerun/vim-polyglot'

Bundle 'juneedahamed/svnj.vim'

Plugin 'simplyzhao/cscope_maps.vim'

" tab 空格
Plugin 'Yggdroot/indentLine'

"配色
Bundle 'joshdick/onedark.vim'

Bundle 'sjl/gundo.vim'

Bundle 'majutsushi/tagbar'

"supertab
"Bundle 'ervandew/supertab'

Bundle 'vim-scripts/taglist.vim'

"Markdown
"Plugin 'godlygeek/tabular'
"Plugin 'plasticboy/vim-markdown'

"airline
Plugin 'vim-airline/vim-airline'
Plugin 'vim-airline/vim-airline-themes'

Bundle 'vim-scripts/sessionman.vim'

"Bundle 'python-mode/python-mode'

Bundle 'rking/ag.vim'

"need vim >= 7.4
" Track the engine.
"Plugin 'SirVer/ultisnips'

" Snippets are separated from the engine. Add this if you want them:
"Plugin 'honza/vim-snippets'

"YouCompleteMe
"Bundle 'Valloric/YouCompleteMe'

" All of your Plugins must be added before the following line
call vundle#end()            " required
filetype plugin indent on    " required

syntax enable
syntax on

nmap <C-A> :w<cr>

" Smart way to move between windows
map <C-j> <C-W>j
map <C-k> <C-W>k
map <C-h> <C-W>h
map <C-l> <C-W>l

set nocompatible
set ic
set incsearch
set hlsearch
set nu
set ignorecase smartcase
set fileencodings=utf-8,gbk,ucs-bom,GB2312,big5

nnoremap <F2> :set number! number?<CR>
nnoremap <F8> :set hlsearch! hlsearch?<CR>
nmap <F3> :cp<cr>
nmap <F4> :cn<cr>
nmap <F6> :cw<cr>
" 粘贴代码时取消自动缩进
set pastetoggle=<F11>

nnoremap ; :

"把 <leader> 设置成空格
let mapleader = "\<Space>"
let g:mapleader = "\<Space>"

" Height of the command bar
set cmdheight=2

set mouse=v
set nobackup
set nowb
set noswapfile

colorscheme onedark
let g:airline_theme='onedark'
set cinoptions=l1
set tabstop=4
set shiftwidth=4
set history=512

filetype on
filetype plugin on
filetype plugin indent on

if empty($TMUXWINIDX)
    let g:airline#extensions#default#layout = [
            \ [ 'a', 'b', 'c' ],
            \ [ 'y', 'z' ]
            \ ]
else
    let g:airline_section_x = $TMUXWINIDX
    let g:airline#extensions#default#layout = [
            \ [ 'a', 'b', 'c' ],
            \ [ 'y', 'z', 'x' ]
            \ ]
endif
let g:airline_section_b = '%-0.10{getcwd()}'


set list
"┊, ¦, ┆, │, ⎸, or ▏
set listchars=tab:\¦\ 

" :IndentLinesToggle
let g:indentLine_showFirstIndentLevel = 1
let g:indentLine_maxLines = 9999
let g:indentLine_first_char = '│'
let g:indentLine_char = '│'

set et
noremap <F9> :set et!<CR>

nnoremap ; :
xnoremap p pgvy

""""""""""""""""""""""""""""""
"lookup file tag file
function! LoadLookUpTag()                                                                                                                                                                                                                   
     "let f1 = expand("%:p:h")
     let f = getcwd()
     let tagsfile =   "/home/zxs/tags/lookuptags/".substitute(f,'/','_','g').".tags"
     let scopefile =  "/home/zxs/tags/lookuptags/".substitute(f,'/','_','g').".cscope_file"
"     if filereadable(lookfile)
"          let g:LookupFile_TagExpr = string(lookfile)
"     endif
     if filereadable(tagsfile)
          execute  "set tags =".tagsfile
     endif
     if filereadable(scopefile)
          execute  "cs add  ".scopefile
     endif
endfunction

au  VimEnter * call LoadLookUpTag()

noremap <silent> bu :BufExplorer<CR>

"for nerdtree
" 设置NERDTree子窗口宽度
let NERDTreeWinSize=32
" 设置NERDTree子窗口位置
let NERDTreeWinPos="right"
" 显示隐藏文件
let NERDTreeShowHidden=1
" NERDTree 子窗口中不显示冗余帮助信息
let NERDTreeMinimalUI=1
" 删除文件时自动删除文件对应 buffer
let NERDTreeAutoDeleteBuffer=1
map <F12> :NERDTreeToggle<CR>

"end nerdtree

" 状态栏显示函数名
fun! ShowFuncName()
    let lnum = line(".")
    let col = col(".")
    echohl ModeMsg
    echo getline(search("^[^ \t#/]\\{2}.*[^:]\s*$", 'bW'))
    echohl None
    call search("\\%" . lnum . "l" . "\\%" . col . "c")
endfun
map f :call ShowFuncName() <CR>

"""""""""""""""""""""""""""""""
"git log
""""""""""""""""""""""""""""""""
nmap :gl :!git gl %<cr>
inoremap gitf  [feature][][]<CR><CR>[what]<CR>[why]null<CR>[how]null<CR><UP><END><UP><UP><UP><UP><Left><Left><Left>
inoremap gitc  [config][][]<CR><CR>[what]<CR>[why]null<CR>[how]null<CR><UP><END><UP><UP><UP><UP><Left><Left><Left>
inoremap gitb  [bugfix][][]<CR><CR>[what]<CR>[why]null<CR>[how]null<CR><UP><END><UP><UP><UP><UP><Left><Left><Left>
inoremap gitm  [merge][][]<CR><CR>[what]<CR>[why]null<CR>[how]null<CR><UP><END><UP><UP><UP><UP><Left><left><left>

inoremap imain    int main(int argc, char *argv[])<CR>{<CR><CR>return 0;<CR>}<CR>

inoremap prk   printk(KERN_EMERG "zxs: %s, %d\n", __func__, __LINE__);

"indent-guides
"随 vim 自启动
let g:indent_guides_enable_on_vim_startup=1
" 从第二层开始可视化显示缩进
let g:indent_guides_start_level=2
" 色块宽度
let g:indent_guides_guide_size=1
" 快捷键 i 开/关缩进可视化
:nmap <silent> <Leader>i <Plug>IndentGuidesToggl

" 自适应不同语言的智能缩进
filetype indent on
" 将制表符扩展为空格
set expandtab
" 设置编辑时制表符占用空格数
set tabstop=4
" 设置格式化时制表符占用空格数
set shiftwidth=4
" 让 vim 把连续数量的空格视为一个制表符
set softtabstop=4

function! Zoom ()
    " check if is the zoomed state (tabnumber > 1 && window == 1)
    if tabpagenr('$') > 1 && tabpagewinnr(tabpagenr(), '$') == 1
        let l:cur_winview = winsaveview()
        let l:cur_bufname = bufname('')
        tabclose

        " restore the view
        if l:cur_bufname == bufname('')
            call winrestview(cur_winview)
        endif
    else
        tab split
    endif
endfunction

nmap <leader>z :call Zoom()<CR>

"GitGutter config
let g:gitgutter_diff_args = '-w'
nmap    gj :GitGutterPrevHunk<CR>
nmap    gk :GitGutterNextHunk<CR>
nmap    gd :GitGutterPreviewHunk<CR>

"ctrlp
let g:ctrlp_map = '<leader>p'
let g:ctrlp_cmd = 'CtrlP'
map <leader>f :CtrlPMRU<CR>
map <leader>o :CtrlPMixed<CR>
let g:ctrlp_custom_ignore = {
    \ 'dir':  '\v[\/]\.(git|hg|svn|rvm)$',
    \ 'file': '\v\.(exe|so|dll|zip|tar|tar.gz|pyc)$',
    \ }
let g:ctrlp_working_path_mode='c'
let g:ctrlp_root_markers = ['.ctrlp']
let g:ctrlp_match_window_bottom=1
let g:ctrlp_max_height=15
let g:ctrlp_match_window_reversed=0
let g:ctrlp_mruf_max=500
let g:ctrlp_follow_symlinks=1

nnoremap <Leader>fu :CtrlPFunky<Cr>
" narrow the list down with a word under cursor
nnoremap <Leader>fU :execute 'CtrlPFunky ' . expand('<cword>')<Cr>
let g:ctrlp_funky_syntax_highlight = 1

let g:ctrlp_extensions = ['funky']

"airline
"设置默认启动
"Thisabled by default; add the following to your vimrc to enable the
"extension:
let g:airline#extensions#tabline#enabled = 1

let g:airline#extensions#tabline#left_sep = ' '
let g:airline#extensions#tabline#left_alt_sep = '|'
"显示 buffer 的数字标签
let g:airline#extensions#tabline#buffer_nr_show = 1

"设置切换Buffer快捷键"
nnoremap bn :bn<CR>
nnoremap bp :bp<CR>

nnoremap <Leader>b :ls<CR>:b<Space>
"end airline

"supertab
"let g:SuperTabDefaultCompletionType="context"
"let g:SuperTabDefaultCompletionType="<C-X><C-O>"
" 0 - 不记录上次的补全方式
" 1 - 记住上次的补全方式,直到用其他的补全命令改变它
" 2 - 记住上次的补全方式,直到按ESC退出插入模式为止
let g:SuperTabRetainCompletionType=2

"gundo
nnoremap <F5> :GundoToggle<CR>

"pymode
let g:pymode_options_max_line_length = 119
let g:pymode_rope_goto_definition_bind = "<C-]>"
let g:pymode_folding = 0 "使能折叠功能
let g:pymode_lint_on_write = 1
"Auto check on save
let g:pymode_lint_write = 1
let g:pymode_doc = 1
let g:pymode_doc_key = 'K'
" syntax highlighting
let g:pymode_syntax = 1
let g:pymode_syntax_all = 1
let g:pymode_syntax_indent_errors = g:pymode_syntax_all
let g:pymode_syntax_space_errors = g:pymode_syntax_all

"tagbar
nmap tb :TagbarToggle<CR>
"TagList
nnoremap <silent> tl :TlistToggle<CR>
"sessionman
set sessionoptions=blank,buffers,curdir,folds,tabpages,winsize
nmap <leader>sl :SessionList<CR>
nmap <leader>ss :SessionSave<CR>
nmap <leader>sc :SessionClose<CR>

" ag
nmap <c-t> :Ag! ""<left>. Ag!

function HeaderPython()
    call setline(1, "#!/usr/bin/python")
    call append(1, "# -*- coding: utf-8 -*-")
    call append(2, "")
    call append(3, "# *************************************************************")
    call append(4, "# Filename @ " . expand("%:t"))
    call append(5, "# Author @ zhengxiasong")
    call append(6, "# Create date @ " . strftime('%Y-%m-%d %T', localtime()))
    call append(7, "# Description @ ") 
    call append(8, "# *************************************************************")
    call append(9, "# Script starts from here")
    normal G
    normal o
endf

autocmd bufnewfile *.py call HeaderPython()

function Headershell()
    call setline(1, "#!/bin/bash")
    call append(1, "")
    call append(2,  "################################################################################")
    call append(3,  "# Copyright Statement: CVTE")
    call append(4,  "# Copyright (C) 2017 Guangzhou Shiyuan Electronics Co.,Ltd. All rights reserved.")
    call append(5,  "#      ____________        _______________  ___________")
    call append(6,  "#     / / ________ \\      / / _____   ____|| |  _______|")
    call append(7,  "#    / / /      \\ \\ \\    / / /   | | |     | | |")
    call append(8,  "#   | | |        \\ \\ \\  / / /    | | |     | | |_______")
    call append(9,  "#   | | |         \\ \\ \\/ / /     | | |     | |  _______|")
    call append(10, "#   | | |          \\ \\ \\/ /      | | |     | | |")
    call append(11, "#    \\ \\ \\______    \\ \\  /       | | |     | | |_______")
    call append(12, "#     \\_\\_______|    \\_\\/        |_|_|     |_|_________|")
    call append(13, "################################################################################")
    call append(14, "# Filename     @ " . expand("%:t"))
    call append(15, "# Author       @ zhengxiasong")
    call append(16, "# Create date  @ " . strftime('%Y-%m-%d %T', localtime()))
    call append(17, "# Description  @ ")
    call append(18, "# version      @ V1.0.0")
    call append(19, "################################################################################")
    call append(20, "# Script starts from here")
    normal G
    normal o
endf

autocmd bufnewfile *.sh call Headershell()


