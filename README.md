GotoPy
======


Python utility to remember commands on MacOSX. 

### Warning
There is a known issue with folders with spaces. 


### Installation
```python

	python goto.py install

```
and just follow instructions

### Uninstallation
```python

	python goto.py uninstall


# or

	goto uninstall

```
and just follow instructions

### Usage

```python

# To add a new entry

goto add <path>::<cmd>::<key>

# example

goto add /Users/username/Documents::cd::doc

# To get the command

goto doc

# List - shows all entries

goto list

# Flush - deletes existing entries

goto flush

```
