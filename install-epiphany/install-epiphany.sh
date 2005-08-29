#install-epiphany
#
#Simple script to fetch epiphany from the repo
#and then remove the install-epiphany trove
#
(
        echo "33"
        conary update epiphany
        echo "66"
        conary erase install-epiphany
        echo "100"
        ) |
        zenity --progress \
          --title="Please Wait" \
          --text="Installing Epiphany..." \
          --auto-close \
          --percentage=0

zenity --info --text="Epiphany has been installed and can be found underneath your Applications/Internet menu."

