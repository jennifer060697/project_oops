from django.shortcuts import render, HttpResponse, redirect
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

def main_page(request) :
    return HttpResponse(f'''
    <html>
    <body>
        <form action="/your_metro/" method="post">
            <p><textarea name="text" placeholder="TEXT"></textarea></p>
            <p><input type="submit"></p>
        </form>
    </body>
    </html>
    ''')

@csrf_exempt
def your_metro(request) :
    if request.method == "POST" :
        text = request.POST['text']
        return HttpResponse(f'''
        {text}
        ''')