mojodemo
========

Upload Excel Files to create Instamojo Offers

### Web Link
http://fathomless-plateau-7249.herokuapp.com/

### Usage
For now users need to be added manually.To add users execute
```shell
python user.py username password
```
Where `username` and `password` are the ones you use for **Instamojo**. Don't worry, I am not storing your password ( see source of `user.py` ).Doing so locally should update the databse on heroku as well.

### Drawbacks

* The site isn't hosted over HTTPS. This is a major security flaw.
* When users are added through `user.py` I am storing the authentication token. If for some reason this is manually deleted all futher uploads will fail. The  alternative is to store the **Instamojo** username and password on the database and generate a new token everytime.
