"""Database host variable."""
from tosh.variable import Variable
from tosh.vars import String


class Host(Variable):
    """Represents a DB Host."""

    prefix = "h"

    def __init__(self, cartosh, hostname):
        """Initialize a host given its hostname."""
        super().__init__(cartosh)
        self._hostname = hostname

    @staticmethod
    async def _load(hostname, task):
        """Load this host from a hostname."""
        return Host(task._tosh, hostname)

    @attributes.register("hostname", String)
    def hostname(self):
        """Name of this database."""
        return self._hostname

    def tokens(self):
        """String representation of the database."""
        return [self._token("{} host".format(self.hostname()))]
