from flows.builtin.webserver.factory import simple_http_server_flow_factory
from jobrunner.post_job import post_job


def run_webserver(port=8080, hierarchy=False):
    """
    Post a job to run a basic webserver to the job board
    :param int port: The port to use for the webserver
    :param bool hierarchy: Print the execution graph
    of the flow that would be posted
    :return None:
    """
    post_job(
        simple_http_server_flow_factory,
        hierarchy=hierarchy,
        store={'port': port},
        capabilities={'port_is_free'}
    )
