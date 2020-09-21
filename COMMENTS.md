#Task description

## Exposing Mailbox as a Filesystem

The goal is to write a daemon (system service) will allows the user to mount and access her mailbox as a synthetic (pseudo) filesystem. Currently only in read-only mode.

Each email message in the mailbox should be represented as a single pseudo file, whose name should be of the form:

`{sender}-{subject}[-{number}]`

(where number is added if there is more than one message with the same name in the directory)

The content of the file should reflect the main content of the email message (incl. headers, but excluding the attachments).

These files should be accessible through the following dynamically-generated directories:

    /timeline/{year}/{month}/{day}/
    /sender/{email}/
    /topics/{IMAP folder path}/ (optional for first implementation)

Implementation notes

- Target platform: Linux, but neatly packed into a docker, so usable easily also on macOS Docker exposes synthesized FS to the host via WebDav (e.g. nginx on local port 8080)
- Language: python
- Read-only mode only
- Live view of the mailbox (i.e. what I see in the FS should correspond to my mailbox content with no more than a few minutes delay)
- The solution will be tested with mailboxes hosted on https://www.fastmail.com


# Comments
First of all - thanks, I really liked this task. I've learned a lot while working on it, eg.:
- how to create custom virtual filesystem in Python
- what syscalls are made by ls and cat

Secondly, I think that my solution isn't the optimal one. If I were to start over, I would go with a different approach:
- mounting my custom FUSE filesystem inside docker and using nginx to serve it via WebDAV works, but seems a bit overengineered (and has the problem of docker container needing more privillages)
- keeping in mind the need for accessing the messages for both reading (by WebDAV server) and writing (by the process that syncs the mailbox) I would probably store them in a database instead of keeping them inside a Python object in memory. 
Either a simple sqlite, or Postgres running in separate docker container.