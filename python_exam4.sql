CREATE TABLE users (id INT PRIMARY KEY AUTO_INCREMENT, name VARCHAR(255), alias varchar(255), email VARCHAR(255), password VARCHAR(255), pw_salt VARCHAR(255), dob DATETIME);

CREATE TABLE quotes (id INT AUTO_INCREMENT PRIMARY KEY, user_id INT, source VARCHAR(255), quote TEXT);

CREATE TABLE favorites (id INT AUTO_INCREMENT PRIMARY KEY, user_id INT, quote_id INT);

INSERT INTO users (name, alias, email, password, pw_salt, dob)
	VALUES (:name, :alias, :email, :password, :pw_salt, :dob)

INSERT INTO quotes (user_id, source, quote)
	VALUES (:user_id, :source, :quote)

INSERT INTO favorites (user_id, quote_id) VALUES(:user_id, :quote_id)


# Get user by email
SELECT name, id, password, pw_salt
	FROM users
	WHERE email=:email;

# Get Count of quotes added
SELECT COUNT(quotes.user_id) AS count FROM quotes WHERE quotes.user_id=:id;

# Get users favorites
SELECT quotes.id AS quote_id, quotes.source AS source, quotes.quote AS quote, users.name AS name, users.id AS id  
	FROM favorites
	LEFT JOIN users ON users.id=favorites.user_id
	LEFT JOIN quotes ON quotes.id=favorites.quote_id
	WHERE favorites.user_id=:id

#Get quotes except those on favorites list
query = SELECT quotes.id AS quote_id, quotes.source AS source, quotes.quote AS quote, users.name AS name, users.id AS id  FROM quotes LEFT JOIN users ON users.id=quotes.user_id WHERE quotes.id NOT IN (SELECT quotes.id AS quote_id FROM favorites LEFT JOIN users ON users.id=favorites.user_id LEFT JOIN quotes ON quotes.id=favorites.quote_id WHERE favorites.user_id=1)"