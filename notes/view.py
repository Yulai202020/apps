from django.http.response import HttpResponse, HttpResponseRedirect
from django.template import Context , Template
from psycopg2 import connect
import random
from django.views.decorators.csrf import csrf_exempt
from django.contrib.sessions.models import Session

conn = connect(host="127.0.0.1",user="yulai",password="qaz123ZX",database="notes")

conn.autocommit = True

MYID = ""

class notes:

    @csrf_exempt
    def login(request):
        with open("html/login.html") as f : html = f.read()
        return HttpResponse(Template(html).render(Context({})))
    @csrf_exempt
    def regis(request):
        with open("html/regis.html") as f : html = f.read()
        return HttpResponse(Template(html).render(Context({})))

    @csrf_exempt
    def view(request,idvid):
        with conn.cursor() as cur:
            cur.execute(f"SELECT ID From accounts where email = '{request.session.get('email')}'")
            MYID = cur.fetchall()[0][0]

        with conn.cursor() as cur:
            cur.execute(f"SELECT * From notes where id = '{idvid}'")
            allnotes = cur.fetchall()[0]
        with open("html/view.html") as f : html = f.read()
        return HttpResponse(Template(html).render(Context({"ID":MYID,"subject":allnotes[1],"text":allnotes[2]})))

    @csrf_exempt
    def index(request) :
        try : request.session['email']
        except : return HttpResponseRedirect("/login/")
        else : return HttpResponseRedirect("/notes")

    @csrf_exempt
    def search(request) :
        
        search = request.POST.get("search")
        selectedtype = request.POST.getlist('typesearch[]')

        with conn.cursor() as cur:
            cur.execute(f"SELECT user_id From accounts where email = '{request.session.get('email')}'")
            MYID = cur.fetchall()[0][0]

        with conn.cursor() as cur:
            if selectedtype == '0':
                cur.execute(f"SELECT * FROM notes WHERE subject LIKE '%{search}%' or content LIKE '%{search}%'")
            elif selectedtype == '1':
                cur.execute(f"SELECT * FROM notes WHERE subject LIKE '%{search}%'")
            else :
                cur.execute(f"SELECT * FROM notes WHERE content LIKE '%{search}%'")
            allnotes = cur.fetchall()
        with open("html/index.html") as f : html = f.read()
        return HttpResponse(Template(html).render(Context({"allnotes":allnotes,"ID":MYID,"a":request.POST.getlist('typesearch')})))

    @csrf_exempt
    def notes(request):
        request.session.get('email')
        with conn.cursor() as cur:
            cur.execute(f"SELECT user_id From accounts where email = '{request.session.get('email')}'")
            MYID = cur.fetchall()[0][0]
        
        with conn.cursor() as cur:
            cur.execute(f"SELECT * From notes where user_id = '{MYID}'")
            allnotes = cur.fetchall()
        with open("html/index.html") as f : html = f.read()
        return HttpResponse(Template(html).render(Context({"allnotes":allnotes,"ID":MYID})))

    @csrf_exempt
    def addhtml(request) :
        with conn.cursor() as cur:
            cur.execute(f"SELECT user_id From accounts where email = '{request.session.get('email')}'")
            MYID = cur.fetchall()[0][0]
        with open("html/add.html") as f : html = f.read()
        return HttpResponse(Template(html).render(Context({"ID":MYID})))

class returns:

    @csrf_exempt
    def logout(request):
        request.session.clear()
        return HttpResponseRedirect("/login/")
    
    @csrf_exempt
    def login(request):
        email = request.POST.get("email")
        password = request.POST.get("password")
        with conn.cursor() as cur:
            cur.execute(f"SELECT user_id From accounts where email = '{email}' and password = '{password}';")
            if cur.fetchall()[0][0] == [] : return HttpResponseRedirect("/login/")
            else :
                MYID = cur.fetchall()
                request.session['email'] = request.POST.get("email")
                request.session['password'] = request.POST.get("password")
                return HttpResponseRedirect("/notes/")

    @csrf_exempt
    def add(request) :
        subject = request.POST.get("sub")
        text = request.POST.get("text")
        with conn.cursor() as cur:
            cur.execute(f"SELECT user_id From accounts where email = '{request.session.get('email')}'")
            MYID = cur.fetchall()[0][0]
        with conn.cursor() as cur:
            cur.execute("insert into notes (\"subject\",\"content\",\"user_id\") values ('{0}','{1}',{2})".format(subject,text,MYID))
        return HttpResponseRedirect('/notes/')

    @csrf_exempt
    def create(request) :
        request.session['email'] = request.POST.get("email")
        request.session['password'] = request.POST.get("password")
        email = request.POST.get("email")
        password =request.POST.get("password")
        rand0 = random.randint(0,9);rand1 = random.randint(0,9);rand2 = random.randint(0,9);rand3 = random.randint(0,9);rand4 = random.randint(0,9);rand5 = random.randint(0,9);rand6 = random.randint(0,9);rand7 = random.randint(0,9);ider = int(str(rand0)+str(rand1)+str(rand2)+str(rand3)+str(rand4)+str(rand5)+str(rand6)+str(rand7))
        with conn.cursor() as cur:
            cur.execute("insert into Accounts(\"email\",\"password\",\"user_id\") values ('{0}','{1}','{2}')".format(email,password,ider))
        MYID = ider
        return HttpResponseRedirect("/notes/")

class datafiles:
    @csrf_exempt
    def stylemincss(self):
        with open("style.min.css","r") as f : return HttpResponse(f.read(),content_type="text/css")