from django.shortcuts import render, redirect
from .models import Organitathion, Account, Tag, AdressOrg, Comment
from .forms import RegisterForm, LoginForm, AddOrgForm, OrgAdressForm, OrgTagForm, CommentForm
from django.contrib import messages

def get_me_org(request):
    # проверка на наличие аккаунта
    me_org = None
    org_id = None
    if request.session.get('auth'):
        if Account.objects.filter(id=request.session.get('account_id')):
            me_org = bool(Account.objects.get(pk=request.session.get('account_id')).organitathion)
            if me_org:
                org_id = Account.objects.get(pk=request.session.get('account_id')).organitathion.id
    return me_org, org_id

def index(request):
    # вывод всех организации
    orgs = Organitathion.objects.all()
    me_org, org_id = get_me_org(request)
    return render(request, 'app/index.html', {'org_id': org_id, 'me_org': me_org, 'orgs': orgs, 'auth': bool(request.session.get('account_id')), 'account_id': request.session.get('account_id')})

def detail(request, pk):
    # вывод организации
    organization = Organitathion.objects.get(pk=pk)
    commentaries = organization.org.all()
    me_org, org_id = get_me_org(request)
    return render(request, 'app/detail.html', {'org_id': org_id, 'org': organization, 'comments': commentaries, 'me_org': me_org, 'auth': bool(request.session.get('account_id')), 'account_id': request.session.get('account_id')})

def tag(request, slug):
    # вывод организации по тегу
    orgs = Organitathion.objects.filter(tages__slug=slug)
    return render(request, 'app/index.html', {'orgs': orgs})

def search_task(request):
    # поиск организации с htmx
    q = request.GET.get('q')
    if q != None:
        tasks = Organitathion.objects.filter(name__iregex=q)
    if q == '':
        tasks = Organitathion.objects.all()
    return render(request, 'app/list_org.html', {'orgs': tasks})

def add_org(request):
    # добавление организации
    if not request.session.get('auth'): 
        return redirect('index')
    formOrg = AddOrgForm()
    formTag = OrgTagForm()
    formAdress = OrgAdressForm()
    if request.method == 'POST':
        # Работа с созданием тегов
        tags = Tag.objects.filter(title__in=[title.replace('\r', '') for title in request.POST.get('title').split('\n')])
        tags = list(tags)
        for el in [title.replace('\r', '') for title in request.POST.get('title').split('\n')]:
            if el not in tags:
                tag = create_tag(el)
                tags.append(tag)
        # Создание адресса
        adress = AdressOrg.objects.create(
            city=request.POST.get('city'),
            street=request.POST.get('street'),
            region=request.POST.get('region'),
            country=request.POST.get('country')
        )
        adress.save()
        # Создание организации
        org = Organitathion.objects.create(
            name=request.POST.get('name'),
            content=request.POST.get('content'),
            web_site=request.POST.get('web_site'),
            phone=request.POST.get('phone'),
            email=request.POST.get('email'),
            photo=request.FILES.get('photo'),
            adress=adress
        )
        org.tages.set(tags)
        a = Account.objects.get(pk=request.session.get('account_id'))
        a.organitathion = org
        a.save()
        org.save()
        return redirect('index')
    me_org, org_id = get_me_org(request)
    return render(request, 'app/add_org.html', {'org_id': org_id, 'formOrg': formOrg, 'formTag': formTag, 'formAdress': formAdress, 'auth': bool(request.session.get('auth')), 'account_id': request.session.get('account_id'), 'me_org': me_org})

def edit_org(request):
    # редактирование организации
    if not request.session.get('auth'):
        return redirect('index')
    me_org, org_id = get_me_org(request)
    a = Account.objects.get(pk=request.session.get('account_id')).organitathion
    formOrg = AddOrgForm(
        instance=a,
    )
    formTag = OrgTagForm({'title': '\n'.join([i.title for i in a.tages.all()])})
    formAdress = OrgAdressForm(instance=a.adress)
    if request.method == "POST":
        # Работа с созданием тегов
        tags = Tag.objects.filter(title__in=[title.replace('\r', '') for title in request.POST.get('title').split('\n')])
        tags = list(tags)
        for el in [title.replace('\r', '') for title in request.POST.get('title').split('\n')]:
            if el not in tags:
                tag = create_tag(el)
                if tag:
                    tags.append(tag)
        # Создание адресса
        adress = AdressOrg.objects.get(pk=Organitathion.objects.get(pk=org_id).adress.id)
        adress.city=request.POST.get('city')
        adress.street=request.POST.get('street')
        adress.region=request.POST.get('region')
        adress.country=request.POST.get('country')
        adress.save()
        # Создание организации
        old_photo = Organitathion.objects.get(pk=org_id).photo
        comments = Comment.objects.filter(organitathion=Organitathion.objects.get(pk=org_id))

        org = Organitathion.objects.create(
            name=request.POST.get('name'),
            content=request.POST.get('content'),
            web_site=request.POST.get('web_site'),
            phone=request.POST.get('phone'),
            email=request.POST.get('email'),
            photo=request.FILES.get('photo') or old_photo,
            adress=adress,
        )
        org.tages.set(tags)
        org.save()
        for i in comments:
            i.organitathion = org
            i.save()
        Organitathion.objects.get(pk=org_id).delete()
        a = Account.objects.get(pk=request.session.get('account_id'))
        a.organitathion = org
        a.save()
        return redirect('index')
    return render(request, 'app/edit_org.html', {'auth': bool(request.session.get('account_id')), 'account_id': request.session.get('account_id'), 'org_id': org_id, 'formOrg': formOrg, 'formTag': formTag, 'formAdress': formAdress, 'me_org': me_org})

def create_tag(el):
    # создание тега
    if el not in [tag.title for tag in Tag.objects.all()]:
        if el != '':
            new_tag = Tag.objects.create(title=el)
            new_tag.save()
            new_tag = Tag.objects.get(pk=new_tag.id)
            return new_tag

def register(request):
    # регистрация
    if request.session.get('auth'):
        red = 'index'
        if request.META.get('HTTP_REFERER'):
            red = request.META['HTTP_REFERER']
        return redirect(red)
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            request.session['account_id'] = Account.objects.get(
                password=form.cleaned_data.get('password'),
                username=form.cleaned_data.get('username')).id
            request.session['auth'] = True
            return redirect('index')
        else:
            messages.error(request, 'Что-то пошло не так')
    else:
        form = RegisterForm()
    me_org, org_id = get_me_org(request)
    return render(request, 'account/register.html', {'org_id': org_id, 'me_org': me_org, "form": form, "auth": bool(request.session.get('auth')), "account_id": request.session.get('account_id')})

def logout(request):
    # выход
    if request.session.get('account_id'):
        del request.session['account_id']
    if request.session.get('auth'):
        del request.session['auth']
    red = 'index'
    if request.META.get('HTTP_REFERER'):
        red = request.META['HTTP_REFERER']
    return redirect(red)

def login(request):
    # вход
    if request.session.get('auth'):
        red = 'index'
        if request.META.get('HTTP_REFERER'):
            red = request.META['HTTP_REFERER']
        return redirect(red)
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')
            if Account.objects.filter(username=username, password=password):
                request.session['account_id'] = Account.objects.get(
                    username=username,
                    password=password
                ).id
                request.session['auth'] = True
                return redirect("index")
        else:
            form = LoginForm()
            messages.error(request, 'Что-то пошло не так')
    me_org, org_id = get_me_org(request)
    return render(request, 'account/login.html', {'org_id': org_id, 'me_org': me_org, "form": LoginForm(), "auth": bool(request.session.get('auth')), "account_id": request.session.get('account_id')})

def add_comment(request, pk):
    # добавление комментария
    form = CommentForm(request.POST)
    org = Organitathion.objects.get(pk=pk)
    if form.is_valid():
        form = form.save(commit=False)
        form.author = request.POST.get('author') or 'Аноним'
        if not request.POST.get('parent', None):
            form.organitathion = org
        form.save()

        if request.POST.get('parent', None):
            parent = Comment.objects.get(pk=request.POST.get('parent'))
            parent.children.add(Comment.objects.get(pk=form.id))
            parent.save()
            Comment.objects.get(pk=form.id).children.set([])
    return redirect('detail', pk)

def delete_comment(request):
    # удаление комментария
    if request.method == 'POST':
        if Comment.objects.filter(id=request.POST['id_com']).exists():
            comment = Comment.objects.get(pk=request.POST['id_com'])
            for i in comment.children.all():
                i.delete()
            comment.delete()
    return redirect('detail', request.POST['org_id'])