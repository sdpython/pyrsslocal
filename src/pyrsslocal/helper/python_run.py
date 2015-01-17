"""
@file
@brief contains functionalities to run a python script
"""
import os, sys


def run_python_script(script, params = { }) :
    """
    execute a script python as a string

    @param  script      python script
    @param  params      params to add before the execution

    @example(compile and run a custom script)
    @code
    fpr = lambda v : self.outStream.write(str(v) + "\n")
    pars = {"print": fpr, "another_variable": 3 }
    run_python_script(script, pars)
    @endcode
    @endexample
    """
    obj = compile(script, "", "exec")

    loc = locals()
    for k,v in params.items() :
        loc [k] = v
    loc["__dict__"] = params

    if "pyrsslocal" not in sys.modules and "pyrsslocal" in script :
        path = os.path.split(__file__)[0]
        path = os.path.join(path, "..","..")
        path = os.path.normpath(os.path.abspath(path))
        sys.path.insert(0,path)
        import pyrsslocal
        rem = True
    else :
        rem = False

    try :
        exec(obj, globals(), loc)

        if rem :
            del sys.path[0]
            del sys.modules["pyrsslocal"]

    except Exception as e :
        if rem :
            del sys.path[0]
            del sys.modules["pyrsslocal"]
        raise e