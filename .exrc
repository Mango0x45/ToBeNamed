au BufNewFile,BufRead *.html setl tw=80
au BufNewFile,BufRead *.md   setl tw=80

inoremap ĳ ij
inoremap Ĳ IJ

nnoremap <leader>f :!pipenv run make format<CR>

let @t = 'i{% trans %}{% endtrans %}k'
let @i = 'i{{ _("") }}4hi'
