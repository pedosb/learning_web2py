@auth.requires_membership('admin')
def create():
   form_presentation = crud.create(db.presentation,
	 next=URL(c='presentations', f='index'))
   response.menu_selected = 'Admin'
   response.title = 'New Presentation'
   return dict(form_presentation = form_presentation)

def list():
   #TODO Make this return ordered by year
   presentations = db().select(db.presentation.ALL,
	 orderby=db.event)
   response.menu_selected = 'Presentations'
   response.title = 'Presentations'
   return dict(presentations = presentations)

def download():
   return response.download(request, db)
