# IP blacklist filter
A simple, high-performance script that filters an NGINX access log based on a 
given blacklist containing CIDR ranges.

IPv4 only. Sorry.

## Install
```bash
pip install -r requirements.txt
pip install -e .
```

## Usage
```bash
blipgrep -f blacklist.txt < access.log
```

You can specify a cache file to avoid recomputing the blacklist. If it exists
already, it will be used **instead** of the blacklist file if given.

```bash
blipgrep -f blacklist.txt -c .cached.json < access.log
```
