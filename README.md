# Stock Calculator Python
```


                                                                   ,-,
                                                             _.-=;~ /_
                                                          _-~   '     ;.
                                                      _.-~     '   .-~-~`-._
                                                _.--~~:.             --.____88
                              ____.........--~~~. .' .  .        _..-------~~
                     _..--~~~~               .' .'             ,'
                 _.-~                        .       .     ` ,'
               .'                                    :.    ./
             .:     ,/          `                   ::.   ,'
           .:'     ,(            ;.                ::. ,-'
          .'     ./'.`.     . . /:::._______.... _/:.o/
         /     ./'. . .)  . _.,'               `88;?88|
       ,'  . .,/'._,-~ /_.o8P'                  88P ?8b
    _,'' . .,/',-~    d888P'                    88'  88|
 _.'~  . .,:oP'        ?88b              _..--- 88.--'8b.--..__
:     ...' 88o __,------.88o ...__..._.=~- .    `~~   `~~      ~-.
`.;;;:='    ~~            ~~~                ~-    -       -   -

```
## Introduction
This stock calculator is built using the PyQt5 framework and is an exercise in understanding event based programming in Python. In attempting to understand this I've applied a modified model view controller (MVC) pattern to this code. This is something I'd like to abstract out into a PyQ5 based opinionated sub-framework.

The MVC pattern introduces the model as a way of modelling our data in a highly reusable way through an exposed well defined API.

The controllers deal with the business logic of handling events from the view, triggered through event handlers on widgets and layouts (our components)

The view is essentially the layout and the widgets that display the output of business logic from the controllers, as well as allowing us to trigger these controllers based on events.

## Documentation
The docs can be found in the `./docs` folder. This provides an overview of all the modules, classes, and available methods.

These docs are generated as HTML and are the recommended inital step in understanding the code.

## Threading
Like any event driven model, there is a GUI thread that handles the UI, however to prevent any interface hangs while we build the model, and process the data, a worker thread is spun up that loads the data into memory.

This continually triggers update signals that allow the loading controller to update the UI in the GUI as this progresses.

## Stock nodes and our data model

The model we use for the data is stored in `app/model/stock`, this loads the data from the `all_stocks_5yr.csv` file in the root at present.

A `StockSource` is used to construct the file, and this has a child class called `StockSourceFile` that implements and overrides the necessary methods to allow us to import from a file.

The `load` method in the `Stock` model constructs a set of `StockNodes` each of which has a `StockValue` for each day, and exposes a set of methods for interacting with this data.

The `StockValue` object provides a set of helper methods for deriving calculations.

The `Stock`, `StockNode`, and `StockValue` intended to be extendable where new methods can be implemented within a controller, with minimum overhead.

![Imgur](https://i.imgur.com/IUfzvH9.png)

## Setup

In the `./bin` directory there is a `setup` script that can be executed when you first clone this repo. This script will deactivate any venv currently running, overwrite the existing venv in the project, and install any required modules from requirements.txt using pip. Finally this will launch the app in the scope of the venv.

```
$ bin/setup
```

Once this has been executed once you can execute the app using `bin/start`.

If you run into any issues with your environment and would like to start over, simply execute again.

## Start
In the `./bin` directory there is a `start` script that can be used to execute the app, this will check the location, deactivate and reactivate the venv, and launch the app in the context of the venv.

```
$ bin/start
```

You can override this running `$ python3 StockCalculator.py`

## Contributing / Building / Extending

In the `./bin` directory there is a `build` script that must be executed before any PR. This is an executable build script that triggers `flake8` checking, linting using `yapf` (applying Google opinionated styling), and generates the documentation.

```
$ bin/build
```

This is a python script that is extendable.

## Support
Any questions, or if you want to discuss further - raise an issue! :heart:


## Roadmap

- Integration testing
- Further abstractions to simplify the app
- Executable building
- Using CI/CD to execute the build
- Abstraction to Framework
- API handling / import file
