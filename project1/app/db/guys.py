"""Moudlo para realizar la conexión a MongoDB."""
from app.db.connection.mongo_conect import Connection


class Guy(Connection):
    """Clase para CRUD de niños del kinder."""

    def __init__(self):
        """Metodo constructor."""
        super().__init__()
        self.collection_guys = self.db['guys']

    def get_guy(self):
        """Método para obtener todos los registros."""
        return self.collection_guys.find()

    def set_guy(self, folio, name, guardian, birthday, gender, age, curp):
        """Método para guardar registro de niño"""
        try:
            self.collection_guys.insert_one(
                {
                    '_id': folio,
                    'name': name,
                    'guardian': guardian,
                    'birthday': birthday,
                    'gender': gender,
                    'age': age,
                    'curp': curp,
                },
            )
            return True
        except Exception:
            return False
            