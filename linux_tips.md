---
layout: kbase_article
title: Guide to the Intel Knights Landing vLab computing cluster
---



# Linux Tips
Use these tricks to speed up your workflow in Linux environments.

----

## Smart arrow keys
At the terminal, pressing the <kbd>↑</kbd> and <kbd>↓</kbd> keys allow you to flip through your bash command history. But you can also configure your environment to filter the history by what you type.

For example, if 5 commands back, you typed a long command like ```git push -f origin HEAD^:master```, you would normally have to hit the <kbd>↑</kbd> key 5 times to call it up.  But you can configure so that you can type in just a tiny bit of the command, like ```gi```, and now pressing <kbd>↑</kbd> will only flip through commands in your history that begin with ```gi```.

To do this, add the following to your ```.bashrc```:
```
bind '"\e[A": history-search-backward'
bind '"\e[B": history-search-forward'
```
Source the file:
```
source ~/.bashrc
```
And you're done!


