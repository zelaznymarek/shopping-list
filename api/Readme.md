## Requirements
* [asdf-vm](https://asdf-vm.com/#/) - Used to set up a local environment with desired runtime versions, e.g. Python@3.9
* [Task](https://taskfile.dev/#/) - Used to run a set of tasks in local environment

## Getting started
### Set up a local environment
1. Set up local environment
```shell
task setup
```

2. Install required dependencies
```shell
task install
```

### Run the app in the local environment
In progress

### Run the app in the docker environment
In order to run the app in the docker environment, firstly build the images:
```shell
task build
```

Secondly you can start the app:
```shell
task run:in-docker
```

To stop the app simply execute:
```shell
task stop:docker
```
## Development

Check code format before committing
```shell
task format
```

## Testing
Tests are run in the docker environment. First, build a docker image:
```shell
task test:build
```

To run tests execute the following command:
```shell
task test
```

In case something goes wrong, and you want to stop the test containers you can do this by executing the following command:
```shell
task test:abort
```
