# Overcooked
Visiting ```http://puzzler7.imaginaryctf.org:9002/``` we get a simple page:
![overcooked-1](overcooked-1.png)

Clicking the link, we get a rare error message:
![overcooked-2](overcooked-2.png)

Investigating the network tab, we can see that the cookies tab is full of "bomb" cookies:
![overcooked-3](overcooked-3.png)

Looking at the storage tab, we can see that there is also a ```access_password``` cookie that likely is necessary to get the flag. 
![overcooked-4](overcooked-4.png)

By removing all of the bomb cookies and refreshing the page, we get the flag.