# What is caddy?

so caddy is a web server helper framework

it helps DNS servers resolve endpoints from the internet

when you navigate to api.vanessa.codes in your browser, it must ask the DNS servers where that domain should ultimately take you.

so in GoDaddy DNS settings we configured a 'A' record that looks like this:


Type | Name | Data
a	   api	  64.181.236.173

So when someone goes to api.vanessa.codes GoDaddy knows to send them to '64.181.236.173' (which is the IP address of your oracle box).

You can check the IP of your box by running `$ curl api.ipify.org` and seeing the result:
```
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
  0     0    0     0    0     0      0      0 --:--:-- --:--:-- --:--:--     0100    14  100    14    0     0    151      0 --:--:-- --:--:-- --:--:--   152
64.181.236.173 # <--- this is your ip!
```

Caddy's config file is located at /etc/caddy/Caddyfile

If you make changes to this config be sure to run `$ caddy reload` to get the freshest version of the config.

If you suspect caddy isn't working try running `$ sudo systemctl status caddy.service` and checking to see if it is active (running).

If it isn't then you probably made an error in the config file.

An example config looks like:

```
api.vanessa.codes {
  reverse_proxy 127.0.0.1:5178
}
```

`reverse_proxy` tells the DNS server where you should end up.


random notes to myself (justin):

had to run
$ sudo firewall-cmd --permanent --add-service=http
and
$ sudo firewall-cmd --permanent --add-service=https

then

$ sudo firewall-cmd --reload

alongside changing the ingress rules in OCI dashboard for the security list to 0.0.0.0/0 TCP ports 80,443 for ingress rules.
