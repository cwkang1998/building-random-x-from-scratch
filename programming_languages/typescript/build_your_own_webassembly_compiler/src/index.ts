import { runtime as compilerRuntime } from './compiler';
import { runtime as interpreterRuntime } from './interpreter';

const apps = [
  { name: 'an empty program', input: '' },
  { name: 'a print statement', input: 'print 8' },
  {
    name: 'multiple statements',
    input: 'print 8 print 24',
  },
  {
    name: 'binary expressions',
    input: 'print(2+4)',
  },
  {
    name: 'nested binary expressions',
    input: 'print ((6-4)+10)',
  },
  {
    name: 'variable declaration',
    input: 'var f = 22 print f',
  },
  {
    name: 'floating point variable assignment',
    input: 'var f = 22.5 f = (f+1.5) print f',
  },
  {
    name: 'while statements',
    input: 'var f = 0 while (f < 5) f = (f + 1) print f endwhile',
  },
  {
    name: 'setpixel statements',
    input: 'setpixel 1 2 3',
  },
];

const display = new Uint8Array(10000);

const compile = async (code: string) => {
  try {
    const tick = await compilerRuntime(code, {
      print: console.log,
      display,
    });
    tick();
  } catch (e) {
    console.error(e);
  }
};

const interprete = async (code: string) => {
  try {
    const tick = await interpreterRuntime(code, {
      print: console.log,
      display,
    });
    tick();
  } catch (e) {
    console.error(e);
  }
};

apps.forEach(async (app) => {
  await compile(app.input);
  // Show display
  display.forEach((value, index) => {
    if (value !== 0) {
      console.log(index, value);
    }
  });
});

// apps.forEach(async (app) => {
//   await interprete(app.input);

//   // Show display
//   display.forEach((value, index) => {
//     if (value !== 0) {
//       console.log(index, value);
//     }
//   });
// });
