from system.core.router import routes
routes['default_controller'] = 'Quotes'
routes['/main'] = 'Quotes#main'
routes['/dashboard'] = 'Quotes#dashboard'
routes['POST']['/register'] = "Quotes#register"
routes['POST']['/signin'] = "Quotes#signin"
routes['POST']['/quotes'] = 'Quotes#addQuote'
routes['/quotes/favorites/<quote_id>'] = 'Quotes#addToFavorites'
routes['/quotes/favorites/remove/<quote_id>'] = 'Quotes#removeFromFavorites'
routes['/users/<id>'] = 'Quotes#getUserInfo'
routes['/logout'] = 'Quotes#logout'
