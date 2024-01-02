from django.shortcuts import render, redirect, HttpResponseRedirect 
from django.urls import reverse
from .forms import VideoUploadForm, WordForm
from .models import UploadedVideo, Subs
from django.core.files.temp import NamedTemporaryFile

from django.conf import settings
import os
from django.core.files import File

from celery.result import AsyncResult


import urllib.request
import tempfile
from pathlib import Path

# from django.core.files.storage import default_storage

from .utils import parse_and_search_subtitles, extract_subtitles


def upload_video(request):
    temp_file = NamedTemporaryFile(delete=True)
    # video_file = tempfile.NamedTemporaryFile(suffix='.mp4')
    video_file = NamedTemporaryFile(delete=True)



    if request.method == 'POST':
        form = VideoUploadForm(request.POST, request.FILES)
        # video_file = request.FILES.get('video')

        if form.is_valid():
            video = form.save()

            # file_path = os.path.join(settings.MEDIA_ROOT, video_file.name)            
            # with open(file_path, 'wb') as f:
            #     for chunk in video_file.chunks():
            #         f.write(chunk)


            # # subtitle_path = os.path.join(settings.MEDIA_ROOT, 'subtitles.srt')

            # # ccextractor_cmd = ['ccextractor', file_path, '-o', subtitle_path]

            # subtitles = extract_subtitles.delay(file_path, temp_file.name)

            
            # os.remove(file_path)

            try:
                urllib.request.urlretrieve(video.video.url, video_file.name) 
                subtitles = extract_subtitles(video_file.name, temp_file.name)

                if subtitles is not None:
                    print("subtitles")
                else:
                    print('Subtitle extraction failed.')

            except Exception as e:
                print(f'Error: {e}')

            # with open(temp_file.name) as f:
            #     content = f.read()
            #     print(content)

            # with open(subtitle_path, "w") as f:
            #     file = File(f)
            s = Subs(video= video)
            filename = Path(f'{video.video.name}').stem
            s.subtitles.save(filename, content=temp_file)
            s.video = video
            s.save()

            # f = open(subtitle_path,"w")
            # file = File(f)

            

            # os.remove(file_path)
            # os.remove(subtitle_path)


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