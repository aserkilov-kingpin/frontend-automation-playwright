import yaml

from common.log_handler import LogHandler

log = LogHandler.get_module_logger(__name__)


def load_yaml(file_name: str) -> dict:
    """Load a YAML file, return it as a dict

    :param file_name: full path to the file to load
    :return: dict representing the YAML contents
    """
    data = None
    result = {}
    with open(file_name, "r") as fh:
        data = fh.read()
    if not data:
        log.error(f"No data found from file {file_name}")
    try:
        result = yaml.safe_load(data)
    except Exception as err:
        line_num = None
        col_num = None
        if hasattr(err, "problem_mark"):
            line_num = err.problem_mark.line
            col_num = err.problem_mark.column
        log.error(f"Problem in yaml {file_name}: line: {line_num} column: {col_num}")
    return result
