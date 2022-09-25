# IP blacklist filter
A simple, high-performance script that filters an NGINX access log based on a 
given blacklist containing CIDR ranges.

IPv4 only. Sorry.

## Usage
```bash
./blacklist_filter.py -b blacklist.txt < access.log
```
The script might spend a lot of time computing the filtering table when using
large ranges. It will generate a `.cached.json` cache file to avoid recomputing
it. If you change the blacklist, delete the cache file.
