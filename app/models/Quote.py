from system.core.model import Model

class Quote(Model):
    def __init__(self):
        super(Quote, self).__init__()

    def get_user_by_email(self, email):
        query = "SELECT * FROM users WHERE email=:email"
        data = {
            'email':email
        }
        rows = self.db.query_db(query,data)
        if len(rows) > 0:
            return rows[0]
        return None

    def create_user(self, info):
        query = "INSERT INTO users (id, name, alias, email, password, pw_salt, dob, created_at, updated_at) VALUES (DEFAULT, :name, :alias, :email, :password, :pw_salt, :dob, NOW(), NOW())"
        data = {
            'name':info['name'],
            'alias':info['alias'],
            'email':info['email'],
            'dob':info['dob'],
            'password':info['password'],
            'pw_salt':info['pw_salt']
        }
        user_id = self.db.query_db(query, data)
        return user_id

    def add_to_favorites(self, id, quote_id):
        query = "INSERT INTO favorites (user_id, quote_id) VALUES(:user_id, :quote_id)"
        data = {
            'user_id': id,
            'quote_id': quote_id
        }
        self.db.query_db(query,data)

    def remove_from_favorites(self, id, quote_id):
        query = "DELETE FROM favorites WHERE user_id=:user_id AND quote_id=:quote_id"
        data = {
            'user_id': id,
            'quote_id': quote_id
        }
        print query
        self.db.query_db(query,data)

    def get_quotes(self, id):
        print 'hello!'
        query = "SELECT quotes.id AS quote_id, quotes.source AS source, quotes.quote AS quote, users.name AS name, quotes.user_id AS id  FROM quotes LEFT JOIN users ON users.id=quotes.user_id WHERE quotes.id NOT IN (SELECT quotes.id AS quote_id FROM favorites LEFT JOIN users ON users.id=favorites.user_id LEFT JOIN quotes ON quotes.id=favorites.quote_id WHERE favorites.user_id=:id)"
        data = {
            'id': id
        }
        quotes = self.db.query_db(query,data);
        return quotes

    def get_quotes_by_user(self, id):
        query = "SELECT * FROM quotes WHERE user_id=:id"
        data = {
            'id': id
        }
        return self.db.query_db(query, data)

    def get_favorites(self, id):
        query = "SELECT quotes.id AS quote_id, quotes.source AS source, quotes.quote AS quote, users.name AS name, quotes.user_id AS id FROM favorites LEFT JOIN users ON users.id=favorites.user_id LEFT JOIN quotes ON quotes.id=favorites.quote_id WHERE favorites.user_id=:id"
        data = {
            'id': id
        }
        favorites = self.db.query_db(query,data)
        return favorites

    def get_count(self, id):
        query = "SELECT COUNT(quotes.user_id) AS count FROM quotes WHERE quotes.user_id=:id"
        data = {
            'id': id
        }
        count = self.db.query_db(query, data)
        return count[0]['count']

    def add_quote(self, data):
        print 'in model'
        query = "INSERT INTO quotes (user_id, source, quote) VALUES (:user_id, :source, :quote)"
        data = {
            'user_id':data['user_id'],
            'quote':data['quote'],
            'source':data['source']
        }
        self.db.query_db(query,data)
        return ''

