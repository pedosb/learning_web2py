
def index():
   #TODO Make this return ordered by year
   publications = db().select(db.publication.ALL,
	 orderby=db.event)
   response.menu_selected = 'Publications'
   response.title = 'Publications'
   return dict(publications = publications)

@auth.requires_membership('admin')
def create():
   form_publication = crud.create(db.publication,
	 next=URL(c='publication', f='index'))
   response.menu_selected = 'Admin'
   response.title = 'New Publication'
   return dict(form_publication = form_publication)

