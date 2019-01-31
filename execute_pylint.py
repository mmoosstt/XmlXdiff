import pylint.lint

root_path = __file__[:__file__.rfind('\\')]

pylint_opts = [
    '--rcfile={path}\\tests\\pylint\\rcfile.txt'.format(path=root_path), 'XmlXdiff']
pylint.lint.Run(pylint_opts)
