au BufNewFile,BufRead *.html setl tw=80
au BufNewFile,BufRead *.md   setl tw=80

inoremap ĳ ij
inoremap Ĳ IJ

let @t = 'i{% trans %}{% endtrans %}k'
