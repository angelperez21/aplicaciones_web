from app.db.connection.mongo_conect import Connection


class User(Connection):
    def __init__(self):
        super().__init__()
        self.collectionUser = self.db['users']

    def getUsers(self):
        return self.collectionUser.find()

    def insert_user(self, user, email, passwd):
        try:
            self.collectionUser.insert_one(
                {'_id': email, 'user': user, 'email': email, 'passwd': passwd}
            )
            return True
        except Exception:
            return False

    def find_user(self, email):
        try:
            return self.collectionUser.find({'_id': email})
        except Exception:
            return 'null'

    def update_user(self, user, email, passwd):
        try:
            filter = {
                '_id': email,
            }
            values = {
                '$set': {
                    '_id': email,
                    'user': user,
                    'email': email,
                    'passwd': passwd,
                }
            }
            return self.collectionUser.update_one(filter, values)
        except Exception as e:
            print(f'Error {e}')
            return False
