# toshql - Sample commands for tosh

This is a sample command package for [tosh](https://github.com/javitonino/tosh). It allows connection to remote postgresql servers via SSH.

## What can I do?

### Variables
 - `db"localhost/mydb"` loads a database by connection string, into an autogenerated variable, `_database`.
 - `mydb = db"localhost/mydb"` loads the database into the `local` variable
 - `local = mydb.host` retrieves the host attribute of the local database
 - You can also paste links (like `psql://localhost/mydb`) to get a variable from that link

### Commands

You can list all databases in a given host by running the `list h"localhost"` command. It return an array of databases in that host, that can be then connected with the `connect` command:

```
> list h"localhost"                                                                                                             
_databases =  [00] postgres DB at localhost                                                                                                                                                                              
 [01] template1 DB at localhost                                                                                      
 [02] template0 DB at localhost                                                                                                      
 [03] test DB at localhost
> test = _databases.3
test = test DB at localhost
> connect test
```

Or you can join everything together in a single command: `connect (list h"localhost").3`
