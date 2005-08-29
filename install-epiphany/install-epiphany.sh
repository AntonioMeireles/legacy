#install-epiphany
#
#Simple script to fetch epiphany from the repo
#and then remove the install-epiphany trove
#
conary update eiphany
conary erase install-epiphany
