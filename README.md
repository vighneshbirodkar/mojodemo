mojodemo
========

Upload Excel Files to create Instamojo Offers

### Web Link
http://fathomless-plateau-7249.herokuapp.com/

### Mock Credentianls
* **Username** - `vighnesh`
* **Password** - `vnb0112`
* [Sample Excel File](https://dl.dropboxusercontent.com/u/74846509/wb.xlsx)

### Usage
For now users need to be added manually.To add users execute
```shell
python user.py username password
```
Where `username` and `password` are the ones you use for **Instamojo**. Don't worry, I am not storing your password ( see source of `user.py` ).Doing so locally should update the databse on heroku as well.

### Drawbacks

* When users are added through `user.py` I am storing the authentication token. If for some reason this is manually deleted all futher uploads will fail. The  alternative is to store the **Instamojo** username and password on the database and generate a new token everytime.
* Storing passwords just by hasing, which can be cracked by brute force. Ideal solution would be to use salted hashes.
* Many others bugs might be lurking, it's my first complete django app.