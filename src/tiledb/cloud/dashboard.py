import logging
import os
import socket
from typing import Any


def panel_dashboard(
    app: Any,
    *,
    full_screen_link: bool = True,
    title="Dashboard - TileDB",
    verbose: bool = False,
    vh_delta: int = 70,
) -> Any:
    """
    Start a Panel server with the provided app and return an iframe that enables
    viewing the app in Voila. This wrapper avoids issues with reactive Panel apps
    in Voila.

    :param app: The Panel app to serve.
    :param full_screen_link: Include a link to the full screen view, defaults to True.
    :param title: Title for the Panel server, defaults to "Dashboard - TileDB".
    :param verbose: Enable verbose logging, defaults to False.
    :param vh_delta: The vertical height delta for the iframe in px. This value is
        subtracted from 100vh to set the height of the iframe.
    :return: A Panel HTML pane containing an iframe that displays the app.
    """

    # Import Panel here to avoid a dependency on Panel.
    import panel as pn

    # Get a random open port.
    with socket.socket() as sock:
        sock.bind(("localhost", 0))
        port = sock.getsockname()[1]

    # Reduce noise from the panel server
    if not verbose:
        logging.getLogger("bokeh").setLevel(logging.CRITICAL)

    # Start the panel server.
    pn.serve(
        app,
        port=port,
        address="localhost",
        show=False,
        title=title,
        websocket_origin="*",
        verbose=verbose,
    )

    # Create the link for the iframe.
    if os.getenv("JUPYTERHUB_API_URL"):
        user = os.getenv("JUPYTERHUB_USER")
        url = f"/user/{user}/proxy/{port}/"
    else:
        url = f"http://localhost:{port}/"

    # Create the iframe.
    html = (
        f"<iframe src='{url}' width='100%' "
        f"style='border: 0;height: calc(100vh - {vh_delta}px);"
        "margin: 0;'></iframe>"
    )

    # Add a link to pop out a full screen view.
    if full_screen_link:
        html += f"\n<a href='{url}' target='_blank'>Full screen view</a>"

    return pn.pane.HTML(html, sizing_mode="stretch_both")
