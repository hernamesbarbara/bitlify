shorten urls quickly from command line using the bitly API. 

install the package with pip

```
git clone git@github.com:hernamesbarbara/bitlyutils.git

cd bitlyutils

pip instsall . 
```

after you installed it, go to bitly.com and find or create an API key 

[https://app.bitly.com/settings/api/oauth/](https://app.bitly.com/settings/api/oauth/)

once you have an API key, copy it to clipboard and save it here:

```

pbpaste > ~/.bitly

```

you are good to go now. 

Usage:

```
# shorten a list of URLs like so
➜  ~ bitlify --csv ~/Desktop/urls.csv

# or shorten a single URL like so
➜  ~ bitlify https://example.com

```

if you pay for custom URLs on bitly, you can use them too like this:

```
# csv has 3 columns: url, title, backhalf
➜  ~ head -n 1  ~/Desktop/urls.csv
url,title,backhalf

➜  ~ bitlify --csv ~/Desktop/urls.csv
1 of 2
https://www.foobar.com => custom.ai/foobar-home
2 of 2
https://www.example.com => custom.ai/example-01
saved 2 results to output.csv

```
