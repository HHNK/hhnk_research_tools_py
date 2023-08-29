from pathlib import Path

import json
from hhnk_research_tools.general_functions import (
    get_functions,
    get_variables,
    ensure_file_path
)

class BasePath:
    
    def __init__(self, base=None):
        self._base = base
        self.path = Path(str(base)).absolute().resolve()

def get_functions(cls):
    funcs = '.'+' .'.join([i for i in dir(cls) if not i.startswith('__') 
                            and hasattr(inspect.getattr_static(cls,i)
                            , '__call__')])
    return funcs
def get_variables(cls):
    variables = '.'+' .'.join([i for i in dir(cls) if not i.startswith('__') 
                            and not hasattr(inspect.getattr_static(cls,i)
                            , '__call__')])
    return variables


# class File(type(Path()), Path):
class File():
    def __init__(self, base):
        self.path = Path(str(base))
    # decorated properties
    @property
    def base(self): #path as posix string (foreward slashes)
        return self.path.as_posix()

    #Path properties
    @property
    def base(self): #full path to file
        return self.path.as_posix()
    @property
    def name(self): #name with suffix
        return self.path.name
    @property
    def stem(self): #stem (without suffix)
        return self.path.stem
    @property
    def suffix(self):
        return self.path.suffix
    def unlink(self, missing_ok=True):
        self.path.unlink(missing_ok=missing_ok)
    @property
    def parent(self):
        return self.path.parent

    def name(self): #name with suffix
        return self.path.name

    @property
    def parent(self):
        return self.path.parent

    #TODO remove in future release
    @property
    def pl(self):
        import warnings
        warnings.warn(".pl is deprecated and will be removed in a future release. Please use .path instead", DeprecationWarning, stacklevel=2)
        return self.path

    def read_json(self):
        if self.path.suffix==".json":
            return json.loads(self.path.read_text())
        else:
            raise Exception(f"{self.name} is not a json.")


    def exists(self):
        """dont return true on empty path."""
        if self.base == ".":
            return False
        else:
            return self.path.exists()
        
    @property
    def path_if_exists(self):
        """return filepath if the file exists otherwise return None"""
        if self.exists():
            return str(self.path)
        else:
            return None

    @property
    def path_if_exists(self):
        """return filepath if the file exists otherwise return None"""
        if self.exists():
            return str(self.path)
        else:
            return None

    # def is_file(self):
    #     return self.path.suffix != ""
    
    def exists(self):
        """dont return true on empty path."""
        if not self._base:
            return False
        else:
            return self.path.exists()

    def __str__(self):
        return self.base
    


class File(BasePath):
    def __init__(self, base):
        super().__init__(base)
        

    #Path properties
    @property
    def stem(self): #stem (without suffix)
        return self.path.stem

    @property
    def suffix(self):
        return self.path.suffix

    def unlink(self, missing_ok=True):
        self.path.unlink(missing_ok=missing_ok)

    def read_json(self):
        if self.path.suffix==".json":
            return json.loads(self.path.read_text())
        else:
            raise Exception(f"{self.name} is not a json.")

    def ensure_file_path(self):
        ensure_file_path(self.path)

    def __repr__(self):
        repr_str = \
f"""{self.path.name} @ {self.path}
exists: {self.exists()}
type: {type(self)}
functions: {get_functions(self)}
variables: {get_variables(self)}
"""
        return repr_str

    def view_name_with_parents(self, parents=0):
        parents = min(len(self.path.parts) - 2, parents) #avoids index-error
        return self.base.split(self.path.parents[parents].as_posix())[-1]
