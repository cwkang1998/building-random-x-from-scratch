# Approach: Building a toy template engine in Python

[Referenced tutorial](http://alexmic.net/building-a-template-engine/l)


## Notes

To run the templating engine, simply do


```bash
python main.py
```

There are two types of tags for this templating language, which is

1. Variables `{{var}}`
2. Blocks `{% each items %} {% end %}`

The engine would be able to handle basic loops and conditional as well as callable python funcs :3

### Loops

```html
{% each people %}
    <div>{it.name}</div>
{% end %}
```

### Conditionals

```html
{% if num > 5 %}
    <div>more than 5</div>
{% else %}
    <div>less than 5</div>
{% end %}
```

### Callables

```html
<div>{% call log 'here' verbosity='debug' %}</div>
````


## Lesson learnt

### Inner workings of templating language

Concept is similar to compilers, in that it also undergoes parsing and tokenization. The difference would probably be that the backend for it would be less complex in comparison with a compiler/intrepreter, as the scope is smaller usually (I think this does depend on the type of templating it is doing, here I am thinking about html based templating language).

### Learnt a lot of built in features and api for pythons

1. raw f strings (Extremely useful)
2. iterators functions, `items()`, `keys()`
3. A lot of useful type annotations

### Type annotations resolution during definition

Learnt about [pep563](https://www.python.org/dev/peps/pep-0563/#rationale-and-goals), and how issues with type resolution is handled for type hints, for referring to classes within that class itself. Interesting to know more about python internals.