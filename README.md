# Welcome to "Fastmail.com" mailbox as a filesystem project!

To use this tool, please build a docker image first. You can do this with this command:

`docker build . -t mailbox`

After build is complete, run the script initial.sh:

`./initial.sh`

After the progress bar reaches 100% you can access your mailbox in your browser at: 

`localhost:8080/`

If you prefer to access your mails using the command line:
1. install the davfs2 package to mount WebDAV as regular filesystem
2. replace default config with the custom one from this project: 
... `sudo cp davfs2.conf /etc/davfs2/davfs2.conf `

3. `sudo mkdir /mnt/mailbox`
4. `sudo mount -t davfs -o noexec localhost:8080 /mnt/mailbox/` 
5. `cd /mnt/mailbox`

To unmount WebDAV: `sudo umount /mnt/mailbox`