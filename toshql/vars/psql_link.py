from urllib.parse import urlparse, parse_qs

from tosh.tasks import task
from tosh.vars.link import register_link

from .database import Database
from .host import Host


@register_link
class PsqlLink:
    """
    Helps load entities represented by PSQL links.
    """

    @staticmethod
    def _link_handler(urlparts):
        path = urlparts.path.strip('/').split('/')
        if path[2] == 'items':
            if len(path) > 3:
                if len(path) > 5 and path[4] == 'occurrences':
                    # https://rollbar.com/user/project/items/12345/instances/123456789/
                    return (RollbarInstance, RollbarLink._load_instance)
                else:
                    # https://rollbar.com/user/project/items/12345
                    return (RollbarItem, RollbarLink._load_item)
            else:
                # https://rollbar.com/user/project/items/?query=search+terms
                return ([RollbarItem], RollbarLink._load_search)
        raise ValueError("Don't know what to do with Rollbar link: " + urlparts)

    @staticmethod
    def return_type(urlparts):
        """Return type depending on the link path."""
        if urlparts.scheme == 'psql':
            if urlparts.path:
                return Database
            else:
                return Host
            return PsqlLink._link_handler(urlparts)[0]

    @staticmethod
    async def _load(url, task):
        urlparts = urlparse(url)
        host = Host(task._tosh, urlparts.netloc)
        if urlparts.path:
            return Database(task._tosh, host, urlparts.path.strip('/'))
        return host
