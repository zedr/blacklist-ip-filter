# IP blacklist filter
A simple, high-performance script that filters an NGINX access log based on a 
given blacklist containing CIDR ranges.

IPv4 only. Sorry.

## Usage
```bash
./blacklist_filter.py -f blacklist.txt < access.log
```

You can specify a cache file to avoid recomputing the blacklist. If it exists
already, it will be used **instead** of the blacklist file if given.

```bash
./blacklist_filter.py -f blacklist.txt -c .cached.json < access.log
```
