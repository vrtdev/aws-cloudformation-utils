import inspect
import os
import socket
import subprocess


def write_template_to_file(template, template_suffix=''):
    """
    Wrapper around write_output_file.

    Additionally adds in some metadata on when/how/where this function was
    called
    :param template: Template to render
    :type template: troposphere.Template
    :param template_suffix: Optional suffix to append to the generated filename
    :type template_suffix: str
    :rtype: None
    """

    build_info = {"built from": {}}

    frames = inspect.getouterframes(inspect.currentframe())
    my_filename = frames[0][1]
    while frames:
        # Skip over all functions in this file
        # Stop at first frame from another file
        if frames[0][1] != my_filename: break

        frames.pop(0)  # next frame

    if frames:
        calling_filename = frames[0][1]
    else:
        calling_filename = None
    del frames  # Needed to avoid circular loops for garbage collection

    # From the python 3.9 change log:
    # Python now gets the absolute path of the script filename specified on the command line [...]
    # As a side effect, the traceback also displays the absolute path for __main__ module frames in this case.
    # Change: bpo-20443 https://bugs.python.org/issue20443
    # We don't want that, so we convert to a relative path (if the path is already relative nothing happens)
    calling_filename = os.path.relpath(calling_filename)

    build_info["built from"]["file"] = calling_filename

    try:
        commit = subprocess.check_output(['git', 'rev-parse', 'HEAD']).strip().decode('utf-8')
        dirty = subprocess.check_output(['git', 'status', '--porcelain'])
        origin = subprocess.check_output(['git', 'remote', 'get-url', 'origin'])

        build_info["built from"]["git info"] = commit
        if dirty != '':
            build_info["built from"]["git info"] += " DIRTY"
        build_info["built from"]["origin"] = origin

    except subprocess.CalledProcessError as e:
        build_info["built from"]["git info"] = "git info could not be retrieved"
        build_info["built from"]["origin"] = "origin could not be retrieved"

    build_info["built on"] = socket.gethostname()
    build_info["url"] = os.environ.get("BUILD_URL", "unknown url")

    try:
        build_info["built by"] = "{name} <{email}>".format(
            name=subprocess.check_output(['git', 'config', 'user.name']).strip().decode('utf-8'),
            email=subprocess.check_output(['git', 'config', 'user.email']).strip().decode('utf-8'),
        )
    except subprocess.CalledProcessError as e:
        build_info["built by"] = os.environ.get("USER", "unknown user")

    template.metadata["Build info"] = build_info
    content = template.to_json()

    calling_filename_parts = os_path_split(calling_filename)
    folder = os_path_join(calling_filename_parts[1:-1])

    filename = '.'.join(os.path.basename(calling_filename).split('.')[:-1]) \
               + template_suffix + '.json'
    write_output_file(folder, filename, content)

    print("   -> Generated {filename}".format(
        filename="output/" + folder + "/" + filename))


def os_path_split(path):
    """
    Split a path with os.path.split(), recursively.

    :param path: The path to split
    :type path: str
    :rtype: List[str]
    """
    rest = path
    components = []
    while rest != '/' and rest != '':
        (rest, last) = os.path.split(rest)
        components.insert(0, last)

    if rest == '/':
        components.insert(0, '/')

    return components


def os_path_join(parts):
    """
    Joins a path with os.path.join(), recursively.

    :param parts: path components
    :type parts: List[str]
    :rtype: str
    """
    if len(parts) == 0:
        return '.'
    elif len(parts) == 1:
        return parts[0]

    folder = parts[0]
    for part in parts[1:]:
        folder = os.path.join(folder, part)

    return folder


def write_output_file(folder, filename, content):
    """
    Write to the output folder, using a subfolder.

    :param folder: The subfolder to put the output in.
    :type folder: str
    :param filename: The file to write to
    :type filename: str
    :param content: The content to write to file
    :type content: str
    :rtype: None
    """
    try:
        os.makedirs('output/{folder}'.format(folder=folder))
    except OSError as e:
        if e.errno != 17:  # This is the File exists error number
            raise
    with open('output/{folder}/{name}'.format(folder=folder, name=filename), 'w') as output_file:
        output_file.write(content)
