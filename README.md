# quiz flask
# Windows / Linux(OsX)  

make venv:
`py -m venv .venv`
`python3 -m venv .venv` 

activate venv:
`.\.venv\Scripts\Activate.ps1`
`source venv/bin/activate`  

install requirements: `pip3 install -r /requirements/main.txt`  
install flake8 with plugins: `pip3 install -r /requirements/flake8.txt`     

change directory to app `cd app` to use `flake8` command

you may install black `pip3 install black` and check code by using `black --check -S --line-length 79 .`
also you can use black to autorefractoring coed by `black -S --line-length 79 .`