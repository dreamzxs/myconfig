#!/usr/bin/expect    
set timeout 5000
set streamStr [lindex $argv 0]
spawn  /opt/cov-analysis-linux64-8.6.0/bin/cov-commit-defects --dir ./cov-lint/ --user admin --password cvtecvte123456 --dataport 9999 --trial-security-file /opt/cov-analysis-linux64-8.6.0/bin/license-trial.dat --host 172.17.84.192 --stream ${streamStr}
expect {
"Enter passphrase for allowing sales engineer to commit trial results:" {send "JD6pjN\r"}
}
expect eof
exit 0

