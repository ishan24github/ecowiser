from django.shortcuts import render, redirect, HttpResponseRedirect 
from django.urls import reverse
from .forms import VideoUploadForm, WordForm
from .models import UploadedVideo, Subs
from django.core.files.temp import NamedTemporaryFile

from django.core.files import File


import urllib.request
import tempfile
from pathlib import Path

# from django.core.files.storage import default_storage

from .utils import parse_and_search_subtitles, extract_subtitles


def upload_video(request):
    temp_file = NamedTemporaryFile(delete=True)
    video_file = tempfile.NamedTemporaryFile(suffix='.mp4')
    # video_file = NamedTemporaryFile(delete=True)

    if request.method == 'POST':
        form = VideoUploadForm(request.POST, request.FILES)

        if form.is_valid():
            video = form.save()

            try:
                urllib.request.urlretrieve(video.video.url, video_file.name) 
                subtitles = extract_subtitles(video_file.name, temp_file.name)

                if subtitles is not None:
                    print("subtitles")
                else:
                    print('Subtitle extraction failed.')

            except Exception as e:
                print(f'Error: {e}')

           
            s = Subs(video= video)
            filename = Path(f'{video.video.name}').stem
            s.subtitles.save(filename, content=temp_file)
            s.video = video
            s.save()


            return HttpResponseRedirect(reverse('upload_video'))
        
    else:
        form = VideoUploadForm()


    videos = UploadedVideo.objects.all()  
    return render(request, 'videoupload/upload_video.html', {'form' : form , 'videos':videos})
    





def processed_video(request, pk):
    temp_file = NamedTemporaryFile(delete=True)

    video = UploadedVideo.objects.get(pk=pk)
    subs = Subs.objects.get(video = pk)

    try:
        urllib.request.urlretrieve(subs.subtitles.url, temp_file.name) 

    except Exception as e:
        print(f'Error: {e}')

        
    if request.method == 'POST':
        form = WordForm(request.POST)
        if form.is_valid():
            word = form.cleaned_data['search_keyword']
            word = word.lower()
            request.session['user_word'] = word
            
            return HttpResponseRedirect(reverse('processed_video' , args=[pk]))
    else:
        form = WordForm()
        word = request.session.get('user_word', None)
        if word:
            matchs, segments = parse_and_search_subtitles(temp_file.name, word)
        else:
            matchs = []
            segments = []


    return render(request, 'videoupload/processed_video.html', {'video' : video,'subs': subs, 'search_word': word, 'matchs': matchs , 'segments': segments, 'form': form})




def delete(request, pk):
     member = UploadedVideo.objects.get(pk=pk)
    #  default_storage.delete(member)                 ### delete from media also
     member.delete()
     return redirect('upload_video')