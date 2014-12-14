from bottle import Bottle, route, run, request, abort
#import bottle_pgsql
#from json import dumps
import json
import datetime
from sqlalchemy import Table, MetaData, create_engine,\
        Column, Integer, Sequence, String, Date
from bottle.ext import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

service_list = {'ssbox',
                'sscloud',
                'ssdb',
                'ssbds',}
secret_code = "He!!034182"

app = Bottle()
#plugin = bottle_pgsql.Plugin('dbname=db user=postgres password=123456')
#app.install(plugin)
#database_url = os.environ["DATABASE_URL"]
database_url = 'postgresql+psycopg2://postgres:123456@localhost/mydb'
engine = create_engine(
	database_url,
        echo=True,
	)
plugin = sqlalchemy.Plugin(
	engine,
	keyword='db')
app.install(plugin)
metadata = MetaData(engine)
#connection = engine.connect()
status_history = Table('status_history', metadata,
	Column('service', String(20), primary_key=True),
	Column('time', Date()),
	Column('status', String(4)),
	Column('from_IP', String(15)),
	Column('message', String),
	)

@route('/api/v1/status/<service_name>', method='PUT')
def update_status( service_name="unkown_service" ):
	if service_name in service_list:
		#data = request.body.readline()
		time_now = str(datetime.datetime.utcnow())
                ip = request.environ.get('REMOTE_ADDR')
		#from_IP = request.headers.get('IP')
		#entity = {status: , message: ,}
		#if not data:
		#	abort(400, 'No data received')
		#print '====================='
		#print data
		#print type(data)
		#print '====================='
		#entity = json.loads(data)
		if not request.forms.get("secret"):
			abort(400, 'No secret code')
		if request.forms.get("secret") == secret_code:
			que = dict()
			que['service'] = service_name
			que['time'] = time_now
			que['status'] = request.forms.get('status')
			que['message'] = request.forms.get('message')
			#que['from_IP'] = '1.1.1.1' # to do: get from http header
			que['from_IP'] = ip
                        i = status_history.insert()
			i.execute(que)
			s = status_history.select()
			rs = s.execute()
			#save_to_database(entity)
		return { "service" : service_name,
				 "success" : True,
				  "time" : time_now,}
	else:
		abort(400, "unkown_service")


#def save_to_database(data_dict, db):
#	db.execute()



if __name__ == '__main__':
	run(host='0.0.0.0', port=8080, debug=True)
