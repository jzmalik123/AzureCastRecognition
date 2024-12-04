from django.shortcuts import render, redirect, HttpResponse

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

