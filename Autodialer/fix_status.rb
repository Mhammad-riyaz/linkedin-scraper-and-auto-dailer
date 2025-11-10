require 'sqlite3'

db = SQLite3::Database.new('db/development.sqlite3')
db.execute("UPDATE calls SET status = 'pending' WHERE status IS NULL")
puts "Fixed NULL status values!"
db.close
