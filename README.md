# SHFQC tool

**Kits for using SHFQC, developed by CCU-QEL Neuro Sama :)**

## Using ccukit

It is recommended to clone the repository or download as zip onto local device for using it:

```sh
git clone https://github.com/CCUQEL/SHFQC.git
```
And please see `use_shfqc_example.ipynb`.

## Importing Examples

```python
import sys
sys.path.insert(0, 'C:\\Users\\user\\Desktop\\py') # add path of where ccukit located
from shfqc import SHFQC
from savekit import *
```
It is recommaned to have the workspace contains the folder of ccukit to see its docstring. For example,
the workspace we used is `C:\Users\user\Desktop\py`, we use VScode to open this folder and use it.


## sub-modules overview
- `shfqc`: Contains SHFQC class for the control object.
- `savekit`: Contains tools to save and read measurement data.
- `use_shfqc_example`: Contains usage example.


> [!NOTE]  
> The used packages like `numpy`, `scipy`, `maplotlib` etc... should be installed by user manually,
> ccukit doesn't provide the check of the installation and version for those packages.
