"""
@file
@brief contains functionalities to run a python script
"""


def run_python_script(script, params=None):
    """
    Executes a script python as a string.

    @param  script      python script
    @param  params      params to add before the execution

    .. exref::
        :title: compile and run a custom script

        ::

            fpr = lambda v : self.outStream.write(str(v) + "\n")
            pars = {"print": fpr, "another_variable": 3 }
            run_python_script(script, pars)
    """
    if params is None:
        params = {}
    obj = compile(script, "", "exec")

    loc = locals()
    for k, v in params.items():
        loc[k] = v
    loc["__dict__"] = params

    try:
        exec(obj, globals(), loc)
    except Exception as e:  # pragma: no cover
        raise e
