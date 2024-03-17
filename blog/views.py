from django.shortcuts import render

from .forms import UserInputForm
from .src import main


def process_input(request):
    scroll_position = request.session.get('scrollPosition', 0)
    if request.method == 'POST':
        form = UserInputForm(request.POST)
        if form.is_valid():
            website_name = form.cleaned_data['option']
            user_input = form.cleaned_data['text_input']
            output = main.main(user_input, website_name)
            context = {'form': UserInputForm(),
                       'output': output.to_dict(orient='records'),
                       'scroll_position': scroll_position}

            return render(request, 'blog/index.html', context)
        else:
            output = None
    else:
        form = UserInputForm()
        return render(request, 'blog/index.html',
                      {'form': form, 'scroll_position': scroll_position})
