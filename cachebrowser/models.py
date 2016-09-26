import peewee
import logging

logger = logging.getLogger(__name__)
db = peewee.SqliteDatabase('')


class BaseModel(peewee.Model):
    pass


class CDN(BaseModel):
    id = peewee.CharField(primary_key=True)
    name = peewee.CharField(null=True)
    edge_server = peewee.CharField(null=True)
    sni_policy = peewee.CharField(null=True)
    valid = peewee.BooleanField(null=False, default=True)
    front = peewee.CharField(null=True)

    class Meta:
        database = db

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.__str__()


class Host(peewee.Model):
    hostname = peewee.CharField(primary_key=True)
    cdn = peewee.ForeignKeyField(CDN, null=True)
    ssl = peewee.BooleanField(default=False)
    is_active = peewee.BooleanField(default=True)
    sni_policy = peewee.CharField(null=True)
    front = peewee.CharField(null=True)

    class Meta:
        database = db

    def __eq__(self, other):
        return self.hostname == other.hostname

    def __str__(self):
        return self.hostname

    def __unicode__(self):
        return self.__str__()


DoesNotExist = peewee.DoesNotExist


def initialize_database(db_filename, reset=False):
    db.database = db_filename

    if reset:
        logger.info("Resetting database tables")
        Host.drop_table(True)
        CDN.drop_table(True)

    CDN.create_table(True)
    Host.create_table(True)

    return db
