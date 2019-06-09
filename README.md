# mprisevent
## MPRIS to HTTP endpoint bridge
Made to send now-playing data from Rhythmbox3 to Icecast2
#### installation:
1. *Clone the repo:*
> **~/ $** `git clone https://github.com/151henry151/mprisevent.git`
2. *Change into the project directory:*
> **~/ $** `cd mprisevent`
3. *Create a venv:*
> **~/mprisevent $** `python3 -m venv env`
4. *Activate the venv:*
> **~/mprisevent $** `source ./env/bin/activate`
5. *Install dependencies:*
> **~/mprisevent $** `python -m pip install .`

#### usage:
`mprisevent.py [-h] url username password`

*_url must include port and full path to metadata source_*

example: 

> **~/mprisevent/mprisevent $** `python mprisevent.py "http://123.45.67.89:1234/admin/metadata" "admin" "password1234"`

Note that nothing will print to the terminal until the next song change.
Note that this will not work in conjunction with ogg Vorbis format streams on Icecast2.
