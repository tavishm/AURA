set mouse-=a 
set ruler
syntax on
set sw=4
set cindent
set ts=4
syntax enable
set hlsearch
set noexpandtab
" Return to last edit position when opening files (You want this!)
   autocmd BufReadPost *
           \ if line("'\"") > 0 && line("'\"") <= line("$") |
     \   exe "normal! g`\"" |
     \ endif

scriptencoding utf-8
set encoding=utf-8

