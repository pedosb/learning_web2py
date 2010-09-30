@auth.requires_membership('admin')
def create():
   form_event = crud.create(db.event,
	 next = URL(c='admin', f='index'))
   response.menu_selected = 'Admin'
   response.title = 'New Event'
   return dict(form_event = form_event)
