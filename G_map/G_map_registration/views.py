from django.shortcuts import render
from django.views.generic import View

# Create your views here.
class Login(View):
    template_name = 'login_page.html'
    form_class = ''

    def get(self, request):
        # form = self.form_class()
        message = ''
        return render(request, self.template_name)
        
    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
            )
            if user is not None:
                login(request, user)
                return redirect('home')
        message = 'Login failed!'
        return render(request, self.template_name, context={'form': form, 'message': message})

        