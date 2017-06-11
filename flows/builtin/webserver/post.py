from flows.builtin.webserver.factory import simple_http_server_flow_factory
from jobrunner.post_job import post_job


def run_webserver(port=8080):
    """
    Post a job to run a basic webserver to the job board
    :param int port: The port to use for the webserver
    :return None:
    """
    post_job(
        simple_http_server_flow_factory,
        store={
            'port': port
        },
        capabilities={'webserver_port_is_free'}
    )
