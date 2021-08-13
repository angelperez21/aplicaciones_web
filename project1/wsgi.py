"""Modulo para poner en marcha el servidor."""

from app.app import app

if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=8000,
        debug=True,
    )
