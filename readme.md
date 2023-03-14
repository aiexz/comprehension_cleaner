# Comprehension Cleaner
This tool allows you to check your code for any unnecessary list comprehensions that can be replaced with generator expression.

## Why?
List comprehensions are great, but they can be a bit slow. If you are using a list comprehension to create a list that is only going to be iterated over once, you can replace it with a generator expression. This will be faster and use less memory.

## How?
> **Warning**
> 
> This tool is in beta, so double check that the information printed is correct before you replace it.

The tool will search through your code and find any list comprehensions that can be replaced with generator expressions. It will print out the line number and the line of code that can be replaced. 

## Example
> **Note**
> 
> Works with python 3.7+, but not tested with other versions.
```python
my_list = [x for x in range(10)]
for x in my_list:
    print(x)
```
```bash
$ python3 -m comprehension_cleaner ./sample
Unnecessary list comprehension in -module.x (lines 1,2), file ./sample/sample.py
```

## Installation & usage
### Poetry
```bash
poetry install
compcleaner ./sample
```
### Python module
```bash
python -m comprehension_cleaner ./sample
```

## TODO
- [ ] Pylint support
- [ ] Flake support
- [ ] Tests?
- [ ] Better output?
- [ ] ~~Better code~~
- [ ] Some documentation
- [ ] Better error handling
## Contributing welcome
### Support
If you find a bug or have a feature request, please open an issue
### Development
If you want to support development, please submit a pull request or star the repo to show your interest.
