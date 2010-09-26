def list():
   projects = db().select(db.project.ALL)
   response.menu_selected = 'Projects'
   return dict(projects=projects)

@auth.requires_membership('admin')
def create():
   form = crud.create(db.project, next=URL(c='projects', f='list'))
   return dict(form=form)
