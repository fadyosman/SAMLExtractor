# SAMLExtractor
A tool that can take a URL or list of URL and prints back SAML consume URL.

## Installation
First you need to install the following packages using your package manager, for example in Ubuntu you can run
```
sudo apt install libxml2-dev libxmlsec1-dev
```

Then you can install python requirements using pip
```
pip install -r requirements.txt
```

## Usage

### Using the login URL directly

The following are examples of the usage, for a single url do
```
./samle.py -u https://carbon-prototype.uberinternal.com/
```

If you have a list you can do
```
./samle.py -U url_list.txt
```

### Using the redirct URL
If you want you can use the redirect URL directly (this doesn't connect to the target server), for a single URL you can use
```
./samle.py -r "https://uber.onelogin.com/trust/saml2/http-post/sso/571434?SAMLRequest=nVNNb9swDP0rhu7%2BkO0iqRAH8FIMC9BtRuLtOjAS2wqwJU%2Bi1%2FTfT3aSIoc1h10siXzie3yiVx76bhD1SC9mh79H9BQd%2B854MScqNjojLHjthYEevSAp9vXXR5EnmRicJSttx6LmvPukjdLm%2Bfa1wwnkxZe2beLm%2B75l0U90XltTsQBg0db7EbfGExgKoYwvY85jXrZZJgouijxAHiqGPC8XRblEDF9eZvcqX4DEXC3v70CpgkW19%2BgoFN5Y48ce3R7dHy3xx%2B6xYi9EgxdpKsEdrInnbuhtwGQ8oNOG0BnoEml7UZZFarWC4FI6%2BfJLnsqx9Wo6ilmvuzLutgFwUcXWFw0wDIk12NlnbSbKmSbtkUABQXq34GVRrtIrthP1IL6F8tuHxnZavkV119nXjUMgrBi5EVn02boe6GNBPOFzRKv4aYYK7EF3tVIOvWfphec8HajmWQl%2BEh4p2th%2BAKf99HR4BEkXS65Rmy50vMOn%2FzHoJkwKOZUO4SYsr9apaRBRBpWtA%2BMH6%2Bhs2r%2F0rE%2B5D3p7z17%2FHOu%2F&RelayState=%2F"
```

Another option is to pass a list of redirect URLs
```
./samle.py -R redirect.txt
```
### Example use case in bug bounty
[https://blog.fadyothman.com/how-i-discovered-xss-that-affects-over-20-uber-subdomains/
](How I Discovered XSS that Affects Over 20 Uber Subdomains)

