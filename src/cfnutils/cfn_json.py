import json
import re
import troposphere
from six import string_types


def cfn_json_dumps(structure):
    """
    Similar to json.dumps(o), but with support for troposphere objects such as:
     - Ref()
     - GetAtt()
     - ImportValue()
     - Sub(), Join()

    Returns a Sub()-wrapped string, with all troposphere-objects pulled to the
    outer layer.

    E.g.:

    cfn_json_dumps({'foo': Sub('${bar}')})
    -> Sub('{"foo", "${bar}"}')

    cfn_json_dumps({'foo': {'bar': Sub('${baz}')}})
    -> Sub('{"foo": {"bar": "${baz}"}})
    """
    def replace_objects(thing, params=None):
        """
        Recursive function to split `thing` into a JSONable object and a dict of
        substitutions.
        :param thing: Thing to split. Probably a dict or list.
        :param params: Params from earlier calls.
        :return: (thing_without_functions, substitutions)
        """
        if params is None:
            params = {}

        if isinstance(thing, string_types):
            # Escape things that look like substitutions
            thing = re.sub(r'\$\{([^}]+)\}', '${!\\1}', thing)
            return thing, params

        elif isinstance(thing, bool) or isinstance(thing, int):
            # Pass through unmodified
            return thing, params

        elif isinstance(thing, dict):
            # Recurse down for keys & values
            _ = {}
            for k, v in thing.items():
                k, params = replace_objects(k, params)
                v, params = replace_objects(v, params)
                _[k] = v
            return _, params

        elif isinstance(thing, list) or isinstance(thing, tuple):
            # Recurse down for every element.
            # We don't need to maintain the list vs tuple, since JSON doesn't
            # differentiate either.
            _ = []
            for e in thing:
                e, params = replace_objects(e, params)
                _.append(e)
            return _, params

        elif isinstance(thing, troposphere.AWSHelperFn):
            # Extract this function by replacing it with a `${}`, and moving it
            # to the outermost Sub()
            aws_function_name = thing.__class__.__name__

            # Find a free name for this kind of function
            sub_name = None
            i = 0
            while sub_name is None or sub_name in params:
                sub_name = "{}_{}".format(aws_function_name, i)
                i = i + 1

            params[sub_name] = thing
            return "${{{}}}".format(sub_name), params

        else:
            raise TypeError("Don't know how to convert {}".format(type(thing)))

    structure, params = replace_objects(structure)
    if params == {}:
        return structure
    else:
        return troposphere.Sub(json.dumps(structure), **params)
