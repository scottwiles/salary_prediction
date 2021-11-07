# Environment Setup

---- 


## Python Environment
1. Open a terminal in the main project directory, create a virtual environment  
`python -m venv .venv`

    a. activate environment with platform specific script, for windows:  
    `.\.venv\Scripts\Activate.ps1`
    
2. Pip install with editable mode to allow import from `./src`  
`pip install -e .`

3. Install dependencies  
`pip install -r requirements.txt`

</br>


```shell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -e .
pip install -r requirements.txt
```

---

## Front-end React Environment
_*Must have node.js insatlled first_

1. Open a terminal in the main project directory, change to `front-end` directory  
`cd front-end`

2. Install the node dependencies  
`npm install`

3. Start local dev mode  
`npm start`

</br>

```shell
cd front-end
npm install
npm start
```
