sudo -u postgres dropdb --if-exists lingojourn_db
sudo -u postgres createdb -O oftg lingojourn_db
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE lingojourn_db TO oftg;"

# sudo psql -U oftg -d lingojourn_db -f backend/createuser.sql -h localhost
