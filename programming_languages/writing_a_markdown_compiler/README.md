# Writing a Markdown Compiler

[Referenced tutorial](https://blog.beezwax.net/2017/07/07/writing-a-markdown-compiler/)

This tutorial was originally written for Ruby, I am just porting it to python beacuse I can xD.

For this markdown compiler, it wouldn't work if you insert special characters (\n, *, _) as a text, e.g. `*Hello world` and `something\n somethingelse` causes syntax error. Tokenizer parses it correctly, parser did not handle this case and cannot comprehend it, resulting in syntax error.

## Lesson Learnt

1. Markdown parsing
2. Quite a nice refresher of CFG and grammar in general