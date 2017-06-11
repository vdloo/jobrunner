from subprocess import check_call, CalledProcessError


def list_tasks_in_flow(flow):
    """
    Return the names of all tasks in the flow
    :param obj flow: The flow to get the tasks from
    :return list task_names: A list of all the task names in a flow
    """
    try:
        return [
            node[0].name for node in flow.iter_nodes()
            if hasattr(node[0], 'name')
        ]
    except StopIteration:
        return list()


def check_nonzero_exit(command):
    """
    Return True or False based on whether the command exited nonzero
    :param str command: shell command to test for a zero exit code
    :return bool exited_zero: True if exited with 0, False if anything else
    """
    try:
        check_call(command, shell=True)
        return True
    except CalledProcessError:
        return False
