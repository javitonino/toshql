"""Commands to open interactive connections."""
from tosh.tasks import Task
from tosh.variable import Variable
from tosh.command import Command
from tosh.ui.vt100_tab import create_interactive_tab
from tosh.lib import ssh

from ..vars.database import Database


class ConnectCommand(Command):
    """Opens interactive connections to postgres consoles."""

    command = 'connect'
    title = 'Opening interactive PSQL console'

    async def _run(self):
        if len(self._arguments) != 1:
            raise TypeError("connect takes one argument: <database>")
        if not isinstance(self._arguments[0], Task):
            raise TypeError("connect second argument must be an expression")
        var = await self.sub(self._arguments[0])
        if not isinstance(var, Variable):
            raise TypeError("connect second argument must be a variable")
        if not isinstance(var, Database):
            raise TypeError("connect second argument must be a Database")
        await self._connect_to_db(var)

    async def _connect_to_db(self, db):
        database_host = await db.attribute("host", self)
        database_hostname = await database_host.attribute("hostname", self)
        database_name = await db.attribute("name", self)
        conn = await self.sub(ssh.get_connection, database_hostname.string)
        session = await self.sub(conn.get_session, ssh.SSHPsqlHandler)
        await self._open_interactive_session(session, database_name.string)

    async def _open_interactive_session(self, session, db_name):
        async with session as handler:
            await self.sub(handler.connect_db, db_name)
            tab = create_interactive_tab(self._tosh, session)

        self._tosh.window.add_tab(tab, switch_to=True)
