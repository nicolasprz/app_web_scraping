from django.shortcuts import render

from .forms import UserInputForm
from .src import main


def process_input(request):
    if request.method == 'POST':
        form = UserInputForm(request.POST)
        if form.is_valid():
            user_input = form.cleaned_data['text_input']
            output = main.main(user_input)
            # If you have a model, you can save the input and output
            # UserInput.objects.create(text_input=user_input, output=output)
        else:
            output = None
    else:
        form = UserInputForm()
        output = None

    return render(request, 'blog/index.html',
                  {'form': form, 'output': output})
