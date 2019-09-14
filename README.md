# NewAlbumScanner
A python script that takes a given users top 50 last.fm artists and checks if they have released an album today.

The Script first reads a last.fm users top 50 artists and then searches spotifys catalogue for any new releases by those artists. 

If any matches are found the script can ping a mobile phone or desktop using notify.run (Web Push API) with the artist, album and a link.

This script was designed to be run through AWS Lambda once a day.
