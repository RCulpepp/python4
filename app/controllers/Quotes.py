from system.core.controller import *
import re, os, hashlib, binascii, datetime

NAME_KEY = re.compile(r'[0-9]')
EMAIL_KEY = re.compile(r'^[a-zA-Z0-9\.\+_-]@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')
class Quotes(Controller):
    def __init__(self, action):
        super(Quotes, self).__init__(action)
        self.load_model('Quote')
        self.db = self._app.db
   
    def index(self):
        session.pop('id', None)
        session.pop('name', None)
        session.pop('alias', None)
        return redirect("/main")

    def main(self):
        # if 'id' in session:
        #     return redirect('/dashboard')
        return self.load_view("index.html")

    def register(self):
        is_valid = True
        for k, v in request.form.items():
            if v == '':
                flash("All fields must be filled in.", "regisError")
                is_valid = False
        user = self.models['Quote'].get_user_by_email(request.form['email'])
        if user != None:
            flash("The email address you entered is already in our system.", "regisError")
            is_valid = False
        if (NAME_KEY.search(request.form['name']) != None) or (NAME_KEY.search(request.form['alias']) != None):
            flash("Names and aliases cannot contain numbers", "regisError")
            is_valid = False
        if len(request.form['name']) < 3 or len(request.form['alias']) < 3:
            flash("Names/Aliases must be longer than 2 characters.", "regisError")
            is_valid = False
        if EMAIL_KEY.match(request.form['email']) != None:
            flash("Email address improperly formatted.", "regisError")
            is_valid = False
        if len(request.form['password']) < 8:
            flash("Passwords must be at least 8 characters.", "regisError")
            is_valid = False
        if request.form['password'] != request.form['confirm-pass']:
            flash("Passwords must match.", "regisError")
            is_valid = False
        if request.form['dob'] > unicode(datetime.datetime.today()):
            flash("Birthdate cannot be in the future.", "regisError")
            is_valid = False
        if not is_valid:
            session['name'] = request.form['name']
            session['alias'] = request.form['alias']
            session['email'] = request.form['email']
            return redirect('/main')
        
        pw_salt = binascii.hexlify(os.urandom(16))
        password = hashlib.sha256(request.form['password'] + pw_salt).hexdigest()

        info = {
            'name':request.form['name'],
            'alias':request.form['alias'],
            'email':request.form['email'],
            'dob':request.form['dob'],
            'password':password,
            'pw_salt':pw_salt
        }

        user_id = self.models['Quote'].create_user(info)
        session['id'] = user_id
        session['alias'] = info['alias']
        return redirect("/dashboard")

    def signin(self):
        user = self.models['Quote'].get_user_by_email(request.form['email'])
        if user == None:
            flash("Email not found in out system.  Please try again.", "signError")
            return redirect('/main')

        if hashlib.sha256(request.form['password'] + user['pw_salt']).hexdigest() != user['password']:
            flash("Password does not match our records.", "signError")
            return redirect('/main')

        session['id'] = user['id']
        session['name'] = user['name']
        return redirect("/dashboard")

    def dashboard(self):
        if 'id' not in session:
            return redirect('/main')
        quotes = self.models['Quote'].get_quotes(session['id'])
        favorites = self.models['Quote'].get_favorites(session['id'])
        return self.load_view('dashboard.html', quotes=quotes, favorites=favorites)

    def addToFavorites(self, quote_id):
        self.models['Quote'].add_to_favorites(session['id'], quote_id)
        return redirect('/dashboard')

    def removeFromFavorites(self, quote_id):
        print 'in controller'
        self.models['Quote'].remove_from_favorites(session['id'], quote_id)
        return redirect('/dashboard')

    def addQuote(self):
        print "in controller"
        is_valid = True
        if len(request.form['source']) < 4:
            flash('Source must be longer than 3 characters', 'createErrors')
            is_valid = False
        if len(request.form['quote']) < 11:
            flash('Source must be longer than 10 characters', 'createErrors')
            is_valid = False
        if not is_valid:
            return redirect('/dashboard')
        quote = {
            'source': request.form['source'],
            'quote': request.form['quote'],
            'user_id': session['id']
        }
        self.models['Quote'].add_quote(quote)
        
        return redirect('/dashboard')


    def getUserInfo(self, id):
        count = self.models['Quote'].get_count(id)
        quotes = self.models['Quote'].get_quotes_by_user(id)
        return load_view('user.html', count=count, quotes=quotes)


    def logout(self):
        if 'id' in session:
            del session['id']
        if 'alias' in session:
            del session['alias']
        return redirect('/main')

