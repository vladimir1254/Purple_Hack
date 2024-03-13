import abc
import math
import subprocess
import logging
from datetime import datetime
from models import PaginationResponse

from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
from cassandra.cqlengine.connection import register_connection, set_default_connection, dict_factory
from cassandra.cqlengine import columns, functions
from cassandra.cqlengine.models import Model

log = logging.getLogger()
log.setLevel('DEBUG')
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s"))
log.addHandler(handler)

HOST = '194.163.137.219'
KEYSPACE = "purple"
HOSTS = [HOST]
CREDENTIAL = {'username': 'cassandra', 'password': 'cassandra'}
AUTH_PROVIDER = PlainTextAuthProvider(username='cassandra', password='cassandra')


class BasePrices(Model):
    __keyspace__ = KEYSPACE
    __table_name__ = 'base_prices'

    location_id = columns.Integer(primary_key=True)
    category_id = columns.Integer(primary_key=True)
    created = columns.DateTime(primary_key=True, default=datetime.utcnow())
    price = columns.Decimal()


class DiscountPrices(Model):
    __keyspace__ = KEYSPACE
    __table_name__ = 'discount_prices'

    location_id = columns.Integer(primary_key=True)
    category_id = columns.Integer(primary_key=True)
    segment_id = columns.Integer(primary_key=True)
    created = columns.DateTime(primary_key=True, default=datetime.utcnow())
    price = columns.Decimal()


def cassandra_session_factory():
    cluster = Cluster(HOSTS, auth_provider=AUTH_PROVIDER)
    session = cluster.connect()

    log.info("Creating keyspace...")
    session.execute("""
        CREATE KEYSPACE IF NOT EXISTS %s
        WITH replication = { 'class': 'SimpleStrategy', 'replication_factor': '2' }
        """ % KEYSPACE
                    )

    log.info("Setting keyspace...")
    session.set_keyspace(KEYSPACE)

    session.row_factory = dict_factory
    session.execute("USE {}".format(KEYSPACE))

    return session


_session = cassandra_session_factory()
register_connection(str(_session), session=_session)
set_default_connection(str(_session))


class AbstractRepository(abc.ABC):

    @abc.abstractmethod
    def to_dict(self, obj):
        raise NotImplementedError

    @abc.abstractmethod
    def to_list(self, l):
        raise NotImplementedError


class BaseRepository(AbstractRepository):
    _model = None

    def __init__(self):
        self.session = _session

    def to_dict(self, obj):
        pass

    def to_list(self, _list):
        if isinstance(_list, list) and len(_list):
            output = []
            for item in _list:
                output.append(self.to_dict(item))
            return output
        else:
            print("A list is reuired!")
            return []

    def _is_empty(self, value):
        if value is None:
            return True
        elif isinstance(value, str) and value.strip() == '':
            return True
        return False

    def find(self, location_id: int, category_id: int):
        item = self._model.objects(location_id=location_id, category_id=category_id)
        if item is not None:
            return dict(item[0])
        return None

    def paginate(self, limit: int, offset: str = None, search: str = ''):
        total = self._model.objects.count()
        last_page = math.ceil(total / limit) if total > 0 else 1
        next_page = None
        data = []

        if total > 0:
            query = self._model.objects.all().limit(limit)

            if offset is not None:
                query = query.filter(pk__token__gt=functions.Token(offset))

            data = list(query)

            if len(data) > 0:
                last = data[-1]
                next_page = f'?limit={limit}&offset={last.pk}&search={search}'

        return PaginationResponse(
            total=total,
            limit=limit,
            offset=offset,
            last_page=last_page,
            next_page_link=next_page,
            data=data
        )

    def create(self, data):
        item = self._model.create(
            location_id=data.location_id,
            category_id=data.category_id,
            created=datetime.utcnow(),
            price=data.price
        )
        return item

    def update(self, location_id: int, category_id: int, data):
        records = self._model.objects(location_id=location_id, category_id=category_id)
        if records is not None:
            item = records[0]
            item.update(
                created=datetime.utcnow(),
                price=data.price
            )
            return item
        return None

    def delete(self, location_id: int, category_id: int, data):
        records = self._model.objects(location_id=location_id, category_id=category_id)

        if records is not None:
            item = records[0]
            item.delete()
            return True
        return False

    def array_query(self, query,segment_id=0):
        result = self.session.execute(query)
        row_dict = {}
        try:
            response = result[-1]
            row_dict = {
                'price': int(response['price']),
                'location_id': response['location_id'],
                'microcategory_id': response['category_id'],
                #'matrix_id': matrix_id,
                'user_segment_id': segment_id
            }
            return row_dict
        except:
            return {}

    def execute(self, query):
        self.session.execute(query)

    def copy_from_csv(self, csv_file_path: str, table: str):

        if table=='discount_prices':
            query = f"COPY {KEYSPACE}.{table} (category_id, location_id, price, created,segment_id)"
        else:
            query = f"COPY {KEYSPACE}.{table} (category_id, location_id, price, created)"    
        query += f" FROM '{csv_file_path}' WITH HEADER = false;"
        command = f"cqlsh {HOST} -e \"{query}\""
        # self.session.execute(query)
        subprocess.run(command, check=True, shell=True, text=True)
        return True
