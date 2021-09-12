# lisp.py

This is based on a tutorial [here](https://khamidou.com/compilers/lisp.py).


## Instructions

To run the interpreter, simple run


```bash
python lisp.py <example.lisp>
```

Note that the interpreter can only evaluate one statement.

## Lesson learnt

Quick tutorial on building lisp. A refresher on programming languages. Learnt more about the operator package, since I never used it before,

Made some changes and modification according to personal preferences:

1. Remove the begin keyword.
2. Change of keyword `define` to  `let`.
3. Some refactoring of the code based on flake8's reccomendation.
4. Added some prints to show the environment after the execution.

Seems that this lisp interpreter doesn't really allow for multi statenent eval, so probably one thing I can extend is maybe build upon this to allow for such evaluation?