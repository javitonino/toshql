"""Commands to open interactive connections."""
from tosh.tasks import Task
from tosh.variable import Variable
from tosh.command import Command
from tosh.vars.basic import List
from tosh.lib import ssh

from ..vars.database import Host, Database


class ListCommand(Command):
    """List databases in a DB host."""

    command = 'list'
    title = 'Listing databases'
    return_type = [Database]

    async def _run(self):
        if len(self._arguments) != 1:
            raise TypeError("list takes one argument: <host>")
        if not isinstance(self._arguments[0], Task):
            raise TypeError("list second argument must be an expression")
        var = await self.sub(self._arguments[0])
        if not isinstance(var, Variable):
            raise TypeError("list second argument must be a variable")
        if isinstance(var, Host):
            host = var
        elif 'host' in var.attributes:
            host = await var.attribute('host', self)
        else:
            raise TypeError("list first argument must be Host or an object with a host attribute")
        return await self._list_dbs(host)

    async def _list_dbs(self, host):
        database_host = await host.attribute("hostname", self)
        conn = await self.sub(ssh.get_connection, database_host.string)
        session = await self.sub(conn.get_session, ssh.SSHPsqlHandler)
        async with session as handler:
            result = await handler.run_command('\pset pager off')
            result = await handler.run_command('SELECT datname FROM pg_database;')
            databases = result.split('\n')[2:-2]
            return List(Database, [Database(self._tosh, host, db.strip()) for db in databases])
