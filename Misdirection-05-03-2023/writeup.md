# Misdirection

We have a zip fiele called ```flag.zip```.

Running ```flag.zip``` reveals that the file's magic bytes show it's a zip archive. 

Trying to unzip it requres a password.

Running ```fcrackzip``` doesn't reveal any password using the rockyou wordlist.

Running ```cat flag.zip``` reveals the flag in the following string:

```
PK
        V-&flag.txtUT   QdQdux
                              ictf{FLAG}PK
        V-&flag.txtUTQdux
                         PKNh
```