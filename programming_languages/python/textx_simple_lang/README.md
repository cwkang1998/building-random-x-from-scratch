# Creating a toy language

This is based on a tutorial for ppci with textx [here](https://ppci.readthedocs.io/en/latest/howto/toy.html)

## Dependencies

This project depends on 2 main packages:

1. textx
2. ppci

textx was used as the frontend for the toy language, and ppci is used as the backend for the toy language.

## Instructions

To run this, simply run `python compiler.py`, and the `example.tcf` file would be compiled into `example.oj` and an `example` executable.

This project is only tested on to run on linux. Might not be able to reproduce this on other machines.

## Lesson learnt

Revised a bit on languages from uni (context free, regular language) and at the same time learnt some components of the underlying backend for a language. `ppci` might be worth discovering for more information regarding the backend.