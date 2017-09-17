"""Database variable."""
from tosh.variable import Variable
from tosh.vars import String

from .host import Host


class Database(Variable):
    """Represents a Database, with a name and a server."""

    prefix = "db"

    def __init__(self, cartosh, host, name):
        """Initialize a cloud given its dictionary from config."""
        super().__init__(cartosh)
        self._host = host
        self._name = name

    @staticmethod
    async def _load(connection_string, task):
        """Load this database from a connection string."""
        parts = connection_string.split('/')
        if len(parts) != 2:
            raise "Invalid syntax for connection string. Try `host/database`."

        return Database(task._tosh, Host(task._tosh, parts[0]), parts[1])

    @attributes.register("name", String)
    def name(self):
        """Name of this database."""
        return self._name

    @attributes.register("host", Host)
    def host(self):
        """Host this database is in."""
        return self._host

    def tokens(self):
        """String representation of the database."""
        return [self._token("{} DB at {}".format(self.name(), self.host().hostname()))]
