
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView
from .models import Announcement, Files, Comments, MyUser, OneTimeCode
from .forms import AnnouncementForm, InputForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin

def register_code_view(request):
    context ={}
    
    if request.method == 'POST' and request.POST.get('Activate') != '':
        #check code
        OneTimeCodeObj = OneTimeCode.objects.filter(User = request.user, Code = request.POST.get('Activate'))
        if OneTimeCodeObj.exists():
            UserObject = MyUser.objects.filter(id = request.user.id)[0]
            UserObject.user_status = True
            UserObject.save()
            OneTimeCodeObj.delete()
            return redirect('/')

    return render(request, "account/register_code.html", context)

class ConfirmedUserMixin:
   
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_superuser or request.user.user_status:
            return super().dispatch(request, *args, **kwargs)
        else:
            return redirect(register_code_view)

def home_view(request):
    context ={}
    context['form']= InputForm()
    if request.method == 'POST':
        form = InputForm(request.POST)
        if request.user.is_authenticated:
            logout(request)
            return render(request, "home.html", context)
        if form.is_valid():
            data = {}
            data['invalid_login'] = False
            cd = form.cleaned_data
            user = authenticate(username=cd['login'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('announce/')
                else:
                    return render(request, 'home.html', context)
            else:
                return render(request, 'home.html', context)
        else:
            return render(request, "home.html", context)
        
    return render(request, "home.html", context)

class AnnounceCreate(ConfirmedUserMixin, CreateView):
    login_url = '/'
    model = Announcement
    template_name = 'announce/announce_create.html'
    fields = ['Announcement_title', 'Announcement_text', 'Category']
    
    def post(self, request, *args, **kwargs):
        
        if request.method == 'POST':
            AnnounceObj = Announcement.objects.create(
                    Announcement_author = request.user,
                    Announcement_title = request.POST['Announcement_title'], 
                    Announcement_text = request.POST['Announcement_text'],
                    Category = request.POST['Category']
                    )

            myFiles = request.FILES.getlist('files')
            if myFiles is not None and len(myFiles) > 0:
                
                for file in myFiles:
                    fileObj = Files.objects.create(Announcement = AnnounceObj, Name = file.name, File = file)
                    fileObj.save()

        return redirect('/announce/')

class AnnouncementList(ListView):
    
    model = Announcement  
    template_name = 'announce/announce.html'
    context_object_name = 'Announcement'
    ordering = ['-Creation_date']
    paginate_by = 10 
    form_class = AnnouncementForm
    queryset = Announcement.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context    

class AnnouncemenDetailView(DetailView):
    
    model = Announcement
    template_name = 'announce/announce_detail.html'
    context_object_name = 'Announcement'
    queryset = Announcement.objects.all()

    def get_object(self):
        obj = super().get_object(queryset=self.queryset)
        return obj
    
    def get_context_data(self, **kwargs): 
        context = super().get_context_data(**kwargs)
        context['form'] = AnnouncementForm()
  
        objFiles= Files.objects.filter(Announcement = self.object)
        data = []
        for file in objFiles:
            file_data =   {'name': file.Name,
                         'type': file.File_type}
            
            data.append(file_data)

        context['dataFiles'] = data
        
        objComments = Comments.objects.filter(Announcement = self.object, Comment_accepted = True)
        data = []
        for comment in objComments:
            data.append(comment)

        context['comments'] = data
        
        return context 

    def post(self, request, *args, **kwargs):
        #Проверка на супер права + проверка на статус активированного аккаунта по коду
        if not request.user.is_superuser:
            if not request.user.user_status:
                return redirect(register_code_view)
        self.object = self.get_object()
        if request.method == 'POST':
            buttonAddCommentPressed = request.POST.get("AddComment")
            if buttonAddCommentPressed is not None and request.POST.get('CommentArea') != "":
                commentObj = Comments.objects.create(Announcement = self.object, User = request.user, Comment = request.POST.get('CommentArea'))
                commentObj.save()

            return redirect('/announce/' + str(kwargs['pk']))

class AnnounceUpdateView(LoginRequiredMixin, UpdateView):
    login_url = '/'
    model = Announcement
    template_name = 'announce/announce_edit.html'
    form_class = AnnouncementForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['Announcement_files'] = Files.objects.filter(Announcement = self.object)
        return context
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(**kwargs)
        
        if request.method == 'POST':
            buttonDeletePressed = request.POST.get("Delete")
            if buttonDeletePressed is not None:
                Files.objects.filter(Announcement = self.object, File = Files.objects.get(id = int(buttonDeletePressed))).delete()
                return redirect('/announce/' + str(kwargs['pk']) + '/edit')
            form = AnnouncementForm(request.POST)
            if form.is_valid():
                files = request.FILES.getlist('files')
                for file in files:
                    fileObj = Files.objects.create(Announcement = self.object, Name = file.name, File = file)
                    fileObj.save()
                
                self.object.save()
                return redirect('/announce/' + str(kwargs['pk']))
            else:
                context['form'] = AnnouncementForm()

        return self.render_to_response(context)

class AnnouncementDelete(LoginRequiredMixin, DeleteView):
    login_url = '/'
    model = Announcement
    template_name = 'announce/announce_delete.html'
    success_url = "/announce/"

class AnnounceComment(LoginRequiredMixin, ConfirmedUserMixin, ListView):
    login_url = '/'
    model = Comments
    template_name = 'announce/announce_comments.html'
    context_object_name = 'Comments'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['AllComments'] = True
        if len(self.kwargs) > 0:
            context['Announcement'] = Announcement.objects.get(id = str(self.kwargs['pk']))
            context['AllComments'] = False
        return context

    def get_queryset(self):
        if "announce" not in self.request.path:
            queryset = Comments.objects.filter(Comment_accepted = False)
        else:
            queryset = Comments.objects.filter(Announcement = Announcement.objects.get(id = str(self.kwargs['pk'])), Comment_accepted = False)
        return queryset
    
    def post(self, request, *args, **kwargs):
        
        if request.method == 'POST':
            pk = None
            buttonAcceptPressed =  request.POST.get("Accept")
            buttonDeniedPressed = request.POST.get("Denied")
            if buttonAcceptPressed is not None:
                objComment = Comments.objects.get(id = buttonAcceptPressed)
                objComment.Comment_accepted = True
                objComment.save()
                pk = objComment.Announcement_id
            elif buttonDeniedPressed is not None:
                objComment = Comments.objects.get(id = buttonDeniedPressed)
                objComment.delete()
            else:
                pass
            
            if pk is not None:
                return redirect('/announce/' + str(pk) +"/comments")
            else:
                return redirect('/announce/' + str(kwargs['pk']) +"/comments")