"""Application entry point — wires FastAPI only; no agent logic here."""

from fastapi import FastAPI

from app.factory import create_app

app: FastAPI = create_app()
