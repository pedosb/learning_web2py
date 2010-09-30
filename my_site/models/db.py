# -*- coding: utf-8 -*- 

#########################################################################
## This scaffolding model makes your app work on Google App Engine too
#########################################################################

if request.env.web2py_runtime_gae:            # if running on Google App Engine
    db = DAL('gae')                           # connect to Google BigTable
    session.connect(request, response, db = db) # and store sessions and tickets there
    ### or use the following lines to store sessions in Memcache
    # from gluon.contrib.memdb import MEMDB
    # from google.appengine.api.memcache import Client
    # session.connect(request, response, db = MEMDB(Client()))
else:                                         # else use a normal relational database
   db = DAL('sqlite://storage.sqlite')       # if not, use SQLite or other DB
## if no need for session
# session.forget()

#########################################################################
## Here is sample code if you need for 
## - email capabilities
## - authentication (registration, login, logout, ... )
## - authorization (role based authorization)
## - services (xml, csv, json, xmlrpc, jsonrpc, amf, rss)
## - crud actions
## (more options discussed in gluon/tools.py)
#########################################################################

from gluon.tools import *
mail = Mail()                                  # mailer
auth = Auth(globals(),db)                      # authentication/authorization
crud = Crud(globals(),db)                      # for CRUD helpers using auth
service = Service(globals())                   # for json, xml, jsonrpc, xmlrpc, amfrpc
plugins = PluginManager()

mail.settings.server = 'logging' or 'smtp.gmail.com:587'  # your SMTP server
mail.settings.sender = 'you@gmail.com'         # your email
mail.settings.login = 'username:password'      # your credentials or None

#auth.settings.hmac_key = 'sha512:23bed6d8-c347-4455-9d6f-9c08fc68ff83'   # before define_tables()
auth.define_tables(username=False)              # creates all needed tables
auth.settings.actions_disabled.append('register')
#auth.settings.mailer = mail                    # for user email verification
#auth.settings.registration_requires_verification = False
#auth.settings.registration_requires_approval = False
#auth.messages.verify_email = 'Click on the link http://'+request.env.http_host+URL(r=request,c='default',f='user',args=['verify_email'])+'/%(key)s to verify your email'
#auth.settings.reset_password_requires_verification = True
#auth.messages.reset_password = 'Click on the link http://'+request.env.http_host+URL(r=request,c='default',f='user',args=['reset_password'])+'/%(key)s to reset your password'

#########################################################################

if request.env.web2py_runtime_gae:            # if running on Google App Engine
   from gluon.contrib.login_methods.gae_google_account import GaeGoogleAccount
   auth.settings.login_form = GaeGoogleAccount()
else:
   from gluon.contrib.login_methods.rpx_account import RPXAccount
   auth.settings.actions_disabled=['register',
	 'change_password','request_reset_password']
   auth.settings.login_form = RPXAccount(request,
	 api_key='1e6a31b03be785473ce0cde0deee66c2cc064bec',
	 domain='pedrobatista',
	 url = "http://192.168.1.2/%s/default/user/login" % request.application)

## If you need to use OpenID, Facebook, MySpace, Twitter, Linkedin, etc.
## register with janrain.com, uncomment and customize following
#from gluon.contrib.login_methods.rpx_account import RPXAccount
#auth.settings.actions_disabled=['register','change_password','request_reset_password']
#auth.settings.login_form = RPXAccount(request,
#      api_key='1e6a31b03be785473ce0cde0deee66c2cc064bec',
#      domain='pedrobatista',
#      url = "http://192.168.1.2/%s/default/user/login" % request.application)
## other login methods are in gluon/contrib/login_methods
#########################################################################

crud.settings.auth = None                      # =auth to enforce authorization on crud

#########################################################################
## Define your tables below (or better in another model file) for example
##
## >>> db.define_table('mytable',Field('myfield','string'))
##
## Fields can be 'string','text','password','integer','double','boolean'
##       'date','time','datetime','blob','upload', 'reference TABLENAME'
## There is an implicit 'id integer autoincrement' field
## Consult manual for more options, validators, etc.
##
## More API examples for controllers:
##
## >>> db.mytable.insert(myfield='value')
## >>> rows=db(db.mytable.myfield=='value').select(db.mytable.ALL)
## >>> for row in rows: print row.id, row.myfield
#########################################################################

#Model for the projects
db.define_table('project',
      Field('title'),
      Field('description', 'text'))

db.project.title.requires = IS_NOT_IN_DB(db, db.project.title)
db.project.description.requires = IS_NOT_EMPTY()

db.define_table('event',
      Field('title'),
      Field('abbreviation'),
      Field('place'),
      Field('year', 'integer'))

db.event.title.requires = IS_NOT_EMPTY()
db.event.abbreviation.requires = IS_NOT_EMPTY()
db.event.place.requires = IS_NOT_EMPTY()
db.event.year.requires = IS_NOT_EMPTY()

db.define_table('publication',
      Field('authors'),
      Field('title'),
      Field('event', db.event))

format_event = lambda e: str(e.abbreviation) + '(' + str(e.year) + ')'

db.publication.title.requires = IS_NOT_IN_DB(db, db.publication.title)
db.publication.authors.requires = IS_NOT_EMPTY()
db.publication.event.requires = IS_IN_DB(db, db.event.id,
      format_event)

db.define_table('presentation',
      Field('title'),
      Field('description', 'text'),
      Field('pdf', 'upload'),
      Field('event', db.event))

db.presentation.title.requires = IS_NOT_EMPTY()
db.presentation.description.requires = IS_NOT_EMPTY()
db.presentation.pdf.requires = IS_NOT_EMPTY()
db.presentation.event.requires = IS_IN_DB(db, db.event.id,
      format_event)
