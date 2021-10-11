# Build your own webassembly compiler (Incomplete)

[Referenced Tutorial](https://blog.scottlogic.com/2019/05/17/webassembly-compiler.html)
[Referenced Repo](https://github.com/ColinEberhardt/chasm)

## Notes

To run the application, do:

```bash
tsc && node build/index.js
```

You can change the code to run using compiler or interpreter.

## Lesson Learnt

1. WASM has a standard, and a set of opscode that we can get from the standard.
2. There's an WebAssembly module for node
3. Difference in implementation method for compilers and intrepreters
4. While loops are quite complex, but with some knowledge of assembly it looks to be quite intuitive.
5. Computer graphics in its simplest form is just....writing to memory and displaying it on screeen (in this case, browser can be be target video out), learnt this during OS lectures in uni, just forgot, good refresher.
6. Learnt about big endian and little endian