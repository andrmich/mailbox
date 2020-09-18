docker run  --rm --device /dev/fuse --cap-add SYS_ADMIN --security-opt apparmor:unconfined  --name klopsik -p 8080:80 klops1

sudo mkdir /mnt/dav

 sudo mount -t davfs -o noexec localhost:8080 /mnt/dav/
