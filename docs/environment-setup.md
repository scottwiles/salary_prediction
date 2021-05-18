# Environment Setup

---- 

1. Within the main project directory create a virtual environment  
`python -m venv .venv`

    a. activate environment with platform specific script, for windows:  
    `.\.venv\Scripts\Activate.ps1`
    
2. Pip install with editable mode to allow import from src  
`pip install -e .`

3. Install packages  
`pip install -r requirements.txt`

---

```shell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -e .
pip install -r requirements.txt
```