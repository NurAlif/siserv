sudo -u postgres dropdb --if-exists lingo_db
sudo -u postgres createdb -O oftg lingo_db
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE lingo_db TO oftg;"

# sudo psql -U oftg -d lingo_db -f backend/createuser.sql -h localhost
