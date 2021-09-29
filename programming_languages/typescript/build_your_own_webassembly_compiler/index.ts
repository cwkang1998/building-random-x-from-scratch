import { runtime } from './compiler';

const apps = [
  { name: 'an empty program', input: '' },
  { name: 'a print statement', input: 'print 8' },
  {
    name: 'multiple statements',
    input: 'print 8 print 24',
  },
  {
    name: 'binary expressions',
    input: 'print(2+ 4)',
  },
  {
    name: 'nested binary expressions',
    input: 'print ((6-4)+10)',
  },
];

const executeCode = async (code: string) => {
  try {
    const tick = await runtime(code, {
      print: console.log,
    });
    tick();
  } catch (e) {
    console.error(e);
  }
};

apps.forEach(async (app) => {
  await executeCode(app.input);
});
