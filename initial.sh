#!/bin/bash

read -p "Please enter your email address: " EMAIL_ADDRESS_INPUT
EMAIL_ADDRESS="$(sed -e 's/[[:space:]]*$//' <<<${EMAIL_ADDRESS_INPUT})"
check=".*@fastmail.com$"
if [[ $EMAIL_ADDRESS =~ $check ]];
then
  read -p "Please enter  password for email address $EMAIL_ADDRESS: "  PASSWORD_INPUT
else
  echo "Please enter an email address from fastmail.com domain."
  exit

fi
 docker run -e "MAILBOX_USERNAME=$EMAIL_ADDRESS" -e "MAILBOX_PASSWORD=$PASSWORD_INPUT" --rm --device /dev/fuse --cap-add SYS_ADMIN --security-opt apparmor:unconfined  --name my_mailbox -p 8080:80 mailbox

