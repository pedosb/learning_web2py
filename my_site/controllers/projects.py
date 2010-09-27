def list():
   projects = db().select(db.project.ALL)
   response.menu_selected = 'Projects'
   response.title = 'Projects'
   return dict(projects=projects)

@auth.requires_membership('admin')
def create():
   form = crud.create(db.project, next=URL(c='projects', f='list'))
   response.menu_selected = 'Admin'
   response.title = 'New Project'
   return dict(form=form)
