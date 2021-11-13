##Requirements
* [asdf-vm](https://asdf-vm.com/#/) - Used to set up a local environment with desired runtime versions, e.g. Python@3.9
* [Task](https://taskfile.dev/#/) - Used to run a set of tasks in local environment

##Getting started
### Set up a local environment
1. Install required asdf-vm plugins
```shell
asdf plugin add python
asdf plugin add poetry
```
2. Install Python
```shell
asdf plugin update python
asdf install python 3.10.0
asdf local python 3.10.0
```
3. Install Poetry
```shell
asdf plugin update poetry
asdf install poetry 1.2.0a1
asdf local poetry 1.2.0a1
```

4. Set up virtualenv using Poetry
```shell
poetry env use python3
```

##Development

Check code format before committing
```shell
poetry run isort backend/app backend/tests
poetry run black backend/app backend/tests
```