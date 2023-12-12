# Connect the dots generator
## Install
To use the program, you need to clone this repository and then install the python dependencies. It is recommended to do so in a virtual environment :
- `python -m venv venv` to create the environment
- `source venv/bin/activate` on Linux and macOS or `.\venv\Scripts\activate` on Windows to activate the environment
- `pip install -r requirements.txt` to install the dependencies.

## Use
**Make sure you activated your virtual environment** (if you used one) before using the program.

Start the program with `python dots.py /path/to/my/background.png`.

There are three modes :
- "add" mode : this is the default mode, a new point is created on click
- "delete" mode : click on existing point to suppress it, press `Esc` to toggle
- "edit" mode : not working for now, press `Space`.

You can :
- press `i` to toggle the background picture
- press `n` to toggle the labels of points

By Rémi Germe.