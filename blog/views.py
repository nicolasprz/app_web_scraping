from django.shortcuts import render

from .forms import UserInputForm


def process_input(request):
    if request.method == 'POST':
        form = UserInputForm(request.POST)
        if form.is_valid():
            # Process the user input and generate the output
            user_input = form.cleaned_data['text_input']
            # Implement your logic to generate the output based on user_input
            output = f"Processed: {user_input}"
            # If you have a model, you can save the input and output
            # UserInput.objects.create(text_input=user_input, output=output)
        else:
            output = None
    else:
        form = UserInputForm()
        output = None

    return render(request, 'blog/template.html',
                  {'form': form, 'output': output})
