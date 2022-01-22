from django.urls import path
from . import view
urlpatterns = [
    # /
    path('', view.notes.index,name="index"),
    path('add/', view.notes.addhtml,name="add"),
    path('notes/', view.notes.notes,name="notes"),
    # regis
    path('regis/', view.notes.regis,name="regis"),
    path('login/', view.notes.login,name="login"),
    # return
    path('loginret/', view.returns.login,name="loginret"),
    path('logout/', view.returns.logout,name="logout"),
    path('return/add', view.returns.add,name="retadd"),
    path('return/creat', view.returns.create,name="create"),
    path('files/stylemincss' , view.datafiles.stylemincss , name="datafiles"),
    path('view/<str:idvid>/' , view.notes.view , name="view"),
]