"""Moudlo para realizar la conexión a MongoDB."""
from app.db.connection.mongo_conect import Connection


class Guy(Connection):
    """Clase para CRUD de niños del kinder."""

    def __init__(self):
        """Metodo constructor."""
        super().__init__()
        self.collection_guys = self.db['guys']

    def get_guys(self):
        return self.collection_guys.find()

    def get_guy(self, folio):
        try:
            return self.collection_guys.find({"_id": folio})
        except Exception:
            return None

    def set_guy(self, folio, name, guardian, birthday, gender, age, curp, grade, email, addrees, tel, tel2):
        """Método para guardar registro de niño"""
        try:
            telephone = []
            telephone.append(tel)
            if len(tel2) != 0:
                telephone.append(tel2)
            self.collection_guys.insert_one(
                {
                    '_id': folio,
                    'name': name,
                    'guardian': guardian,
                    'birthday': birthday,
                    'gender': gender,
                    'age': age,
                    'curp': curp,
                    'grade': grade,
                    'email': email,
                    'address': addrees,
                    'telephone': telephone,
                },
            )
            return True
        except Exception:
            return False
        

    def update_guy(self, folio, name, guardian, birthday, gender, age, curp, grade, email, addrees, tel, tel2):
        filter = {
            "_id": folio,
        }
        telephone = []
        telephone.append(tel)
        if len(tel2) != 0:
            telephone.append(tel2)
        values = {
            "$set": {
                "name": name,
                "guardian": guardian,
                "birthday": birthday,
                'gender': gender,
                'age': age,
                'curp': curp,
                'grade': grade,
                'email': email,
                'addrees': addrees,
                'telephone': telephone
            },
        }
        try:
            return self.collection_guys.update_one(filter, values)
        except Exception as e:
            print(f"Error {e}")
            return False
