from django.shortcuts import render, redirect, HttpResponse
from .services.azuracast_client import AzuraCastClient
from .services.music_info_client import MusicInfoClient

from .services.music_brainz_client import MusicBrainzClient

# Create your views here.
def home(request):

    return render(request, 'home.html')
    # tools = AiTools.objects.filter(is_reviewed=True)
    # sort_key = ToolsSettings.objects.filter(key='sort_tools').first()
    #
    # unordered_tools = tools.filter(position__isnull=True)
    # ordered_tools = tools.filter(position__isnull=False).order_by('position')
    #
    # if sort_key:
    #     sort_key = sort_key.value
    #     unordered_tools = unordered_tools.order_by(sort_key)
    #
    # tools = list(ordered_tools) + list(unordered_tools)
    # tags = taghelper.objects.values('tag_text').distinct().exclude(Q(tag_text__isnull=True) | Q(tag_text='') | Q(tag_text="Matt's Picks") | ~Q(tag_text__regex=r'^[A-Z]'))
    # video_url = ToolsSettings.banner_video_url()
    # banner_image_src = ToolsSettings.banner_image_src()
    # banner_image_url = ToolsSettings.banner_image_url()
    #
    # page_number = request.GET.get('page')
    # page_obj = p.get_page(page_number)
    #
    # context = {
    #     'tools': page_obj,
    #     'tags': tags,
    #     'video_url': video_url,
    #     'banner_image_src': banner_image_src,
    #     'banner_image_url': banner_image_url
    # }

def login(request):

    return render(request, 'login.html')

def automatic_detection(request):
    now_playing = AzuraCastClient().now_playing()
    song_name = now_playing['title']
    artist_name = now_playing['artist']

    music_client = MusicInfoClient()
    artist_details = music_client.get_artist_data(artist_name)
    artist_details = artist_details['lastfm'] or artist_details['wikipedia'] or artist_name

    song_details = music_client.get_song_data(artist_name, song_name)
    song_details = song_details['lastfm'] or song_name

    band_details = music_client.get_band_data(artist_name)

    context = {
        "song_details" : song_details,
        "artist_details" : artist_details,
        "band_details" : band_details
    }
    return ""


def manual_detection(request):
    now_playing = AzuraCastClient().now_playing()
    song_name = now_playing['title']
    artist_name = now_playing['artist']

    music_client = MusicInfoClient()
    artist_details = music_client.get_artist_data(artist_name)
    artist_details = artist_details['lastfm'] or artist_details['wikipedia'] or artist_name

    song_details = music_client.get_song_data(artist_name, song_name)
    song_details = song_details['lastfm'] or song_name

    band_details = music_client.get_band_data(artist_name)['open_ai']

    context = {
        "song_details": song_details,
        "artist_details": artist_details,
        "band_details": band_details
    }

    return render(request, 'manual_detection.html', context)
