# Adding an SSH User on HELPS

The HELPS computer is accessible over the Internet on 128.46.75.64. This poses a security risk, since the HELPS computer is vulnerable to malicious attacks. As the number of members on the CAM2 team increases, the vulnerability of the
HELPS machine increases too. This is because the chance a malicious program will guess a username on the server increases. Once a username is guess, a NVIDIA Titan X graphics card can hack any password (8 characters or less) in under 24 hours.

In order to avert security risk, the CAM2 team requires users to login using ssh-keys. This document outlines how the process is run. The two main parties involved are a "Sys Admin" (or System Administrator) and a "New User". This is a distillation of these two articles on [Adding an Ubuntu User](https://www.digitalocean.com/community/tutorials/how-to-create-a-sudo-user-on-ubuntu-quickstart) and [Managing SSH Keys](https://help.github.com/articles/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent/).

**Note**: Generally, the "username" is the new users Purdue ID.
**Note**: The IP Address of 128.46.75.64 is referred to as `helps`.


## (Sys Admin) Creating New Username

```Shell
adduser username
```

It will prompt you for a password. It is okay to give them a simple password like "1234". In the near future, the user will not be able to login via password anyway.

Next we need to add the user to the group they are a member of, so they can access all their team's shared files. This is run as:

```Shell
usermod -aG group_name_here username
```

Notice: Do NOT add anyone as a "sudo" user unless you are given explicit permission.

## (Sys Admin) Creating SSH Key-Pairs

Next on the local machine of the system administrator, the ssh key-pairs will be generated. 

```Shell
ssh-keygen -t rsa -b 4096 -C "your_email@purdue.edu"
```

It will ask the path to save the new SSH key. Give the full path to some directory where you, the System Admin, can keep track of the files. It is recommended to save it to:

```
/home/the_sys_admin_username/my_keys/username_of_new_user
```

The private key (no .pub) and public key (with .pub) are now generated.


## (Sys Admin) Add SSH Key to New User

Now we add the ssh key to the new user's account.

```Shell
ssh-copy-id -i path_to_new_ssh_key/private_key_no_pub new_user_username@128.46.75.64
```
 
It may ask you to say "yes" or something, which is okay to do.


## (Sys Admin) Remove Password Login

Now to only allow a user to login via ssh-key pairs, we modify the sshd program (the service allowing ssh on the server).

```Shell
emacs /etc/ssh/sshd_config
```

Near the end of the file, there is a long list of usernames with the following config information below them. Add the "new_user_username" to the end of the comma-separated list.

```
Match User example_user_name,new_user_username
     PasswordAuthentication no
     RSAAuthentication yes
     PubkeyAuthentication yes
     AuthorizedKeysFile %h/.ssh/authorized_keys
```

Restart the sshd service:

```Shell
sudo service sshd restart
```

Verify this by sshing into the user account from your local machine:

```Shell
ssh -i <path_to_key>/new_user_username new_user_username@128.46.75.64
```

You should be able to login. Now try:

```Shell
ssh new_user_username@128.46.75.64
```

It should fail.


## (Sys Admin) Give SSH Keys to New User


Now send both ssh keys to the new user. Slack is a good choice.


## (New User) Download the SSH Keys

Download the keys to your computer. Add these to your `~/.ssh/` directory.

Importantly, the permissions are not set correctly at this time on your `new_user_username` private key file. To set the permissions run:

```Shell
chmod 600 new_user_username
```

## (New User) Add SSH Key to Local Account

For convenience, let us add the new ssh key to our local ssh program.

```Shell
ssh-add ~/.ssh/new_user_username
```

To verify run:

```Shell
ssh-add -l
```

You should see your new key listed.

## (New User) Add "helps" to local DNS

The ip address `128.46.75.64` is not easy to remember. Instead, let us add it to our local computer's DNS.

```Shell
emacs /etc/hostname
```

Add this line to the end (note the "tab" not a "space"):

```
128.46.75.64	helps
```

To verify, run:

```Shell
ping helps
```

It should get responses.


## (New User) Does it all Work?


Now to login securly to HELPS, run:

```Shell
ssh new_user_username@helps
```

All should work!





