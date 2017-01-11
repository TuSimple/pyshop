#coding=utf-8
"""
PyPI XML-RPC Client helper

To use the :data:`pyshop.helpers.pypi.proxy`, the method
:method:`pyshop.helpers.pypi.set_proxy`must be called to
install the XML RPC proxy.

Also it is possible to install an HTTP Proxy in case the pyshop host does not
have a direct access to internet.

This is actually a configuration key ``pyshop.pypi.transport_proxy`` from the
paste ini file.

.. warning::
    This code use an unsecured connection (http)
    and should be modified since PyPI is available in https.

.. :data:`proxy`:: The XML RPC Proxy


"""
try:
    import xmlrpc.client as xmlrpc
except ImportError:
    import xmlrpclib as xmlrpc

import requests

proxy = None


class RequestsTransport(xmlrpc.Transport):
    """
    Drop in Transport for xmlrpclib that uses Requests instead of httplib

    # https://gist.github.com/chrisguitarguy/2354951
    """
    # change our user agent to reflect Requests
    user_agent = "PyShop"

    def __init__(self, use_https):
        xmlrpc.Transport.__init__(self)  # Transport does not inherit object
        self.scheme = 'https' if use_https else 'http'

    def request(self, host, handler, request_body, verbose):
        """
        Make an xmlrpc request.
        """
        headers = {'User-Agent': self.user_agent,
                   #Proxy-Connection': 'Keep-Alive',
                   #'Content-Range': 'bytes oxy1.0/-1',
                   'Accept': 'text/xml',
                   'Content-Type': 'text/xml' }
        url = self._build_url(host, handler)
        try:
            resp = requests.post(url, data=request_body, headers=headers)
        except ValueError:
            raise
        except Exception:
            raise # something went wrong
        else:
            try:
                resp.raise_for_status()
            except requests.RequestException as e:
                raise xmlrpc.ProtocolError(url, resp.status_code,
                                                        str(e), resp.headers)
            else:
                return self.parse_response(resp)

    def parse_response(self, resp):
        """
        Parse the xmlrpc response.
        """
        p, u = self.getparser()
        p.feed(resp.content)
        p.close()
        return u.close()

    def _build_url(self, host, handler):
        """
        Build a url for our request based on the host, handler and use_http
        property
        """
        return '%s://%s%s' % (self.scheme, host, handler)



def set_proxy(proxy_url, transport_proxy=None):
    """Create the proxy to PyPI XML-RPC Server"""
    global proxy
    proxy = xmlrpc.ServerProxy(
        proxy_url,
        transport=RequestsTransport(proxy_url.startswith('https://')),
        allow_none=True)

from multiprocessing.dummy import Pool as ThreadPool

def fetch(args):
    package_name,release = args
    release_data = proxy.release_data(package_name, release)
    release_files = proxy.release_urls(package_name, release)
    return (release_data,release_files)

def synchronous():
    package_name="requests"
    releases = proxy.package_releases(package_name, True)
    for r in releases:
        fetch(package_name,r)

def asynchronous(package_name,releases):

    # package_name="requests"
    # releases = proxy.package_releases(package_name, True)
    if len(releases) > 0 :
        pool = ThreadPool(len(releases))
        # Open the urls in their own threads and return the results
        results = pool.map(fetch, [(package_name,version) for version in releases])
        #close the pool and wait for the work to finish
        pool.close()
        pool.join()
    else:
        results = []

    return results