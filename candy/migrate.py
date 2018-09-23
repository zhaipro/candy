from playhouse import migrate
import jwt

import orm


migrator = migrate.SqliteMigrator(orm.db)

migrate.migrate(
    migrator.add_column('user', 'expires', migrate.IntegerField(default=0)),
    migrator.add_column('user', 'uid', migrate.IntegerField(null=True)),
)


for user in orm.User.select():
    payload = jwt.decode(user.token, verify=False)
    user.expires = payload['exp']
    user.uid = payload['id']
    user.save()
