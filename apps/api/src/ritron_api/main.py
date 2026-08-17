"""ASGI entry point for the RITRON API foundation."""

from ritron_api.app import create_app

app = create_app()
