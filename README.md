install

```
git clone git@github.com:hernamesbarbara/bitlify.git

cd bitlify

pip instsall . 
```

find or create an API key on bitly

[https://app.bitly.com/settings/api/oauth/](https://app.bitly.com/settings/api/oauth/)

save API key here:

```

pbpaste > ~/.bitly

```

good to go 


```
# shorten a list of URLs like so

bitlify --csv ~/Desktop/urls.csv

# or shorten a single URL like so
bitlify https://example.com

```
