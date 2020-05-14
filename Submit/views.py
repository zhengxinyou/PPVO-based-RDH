import numpy as np
from PIL import Image
from django.http import HttpResponse
from django.shortcuts import render
from Submit import rdhhelper,tools

# Create your views here.
from django.views.generic import TemplateView


from RDHWeb.settings import MEDIA_URL_PREFIX, MEDIA_ROOT
from Submit.models import NoEmbed


def index(request):
    return HttpResponse('index')


class UploadView(TemplateView):
    template_name = "sub.html"

    def post(self, request):

        img = request.FILES.get('img')
        im_pic = Image.open(img)
        x = np.array(im_pic, dtype=np.int32)

        embed_info = request.POST.get('embedInfo')

        embed_success, extract_img, psnr, embed_stages = rdhhelper.embed_main(x, -1, -1, 10, embed_info)

        if not embed_success:
            return render(request, 'notEnoughCapacity.html')

        new_im = Image.fromarray(extract_img.astype(np.uint8))
        new_im.save('static/imgs/noembeds/result.bmp')

        return render(request, 'imgshow.html', context={"image_url": MEDIA_URL_PREFIX + 'noembeds/result.bmp',
                                                        "psnr":psnr,
                                                        "stage":embed_stages})


def get_image(request):
    i = NoEmbed.objects.last()
    i_name = i.i_name

    return render(request, 'imgshow.html', context={"image_url": MEDIA_URL_PREFIX + 'noembeds/result.bmp',
                                                    "image_name": i_name})


def read_image(img_path):
    i = Image.open(img_path)
    # i.show()
    x = np.array(i, dtype=np.int32)
    return x


# for test
class getInfoView(TemplateView):
    template_name = "getinfo.html"

    def post(self, request):
        img = request.FILES.get('img')
        originimage = request.FILES.get('originimage')
        imgname = request.POST.get('imagename')

        im_pic = Image.open(img)
        originimg = Image.open(originimage)

        x = np.array(im_pic, dtype=np.int32)
        ori_x = np.array(originimg, dtype=np.int32)

        recover_info, recover_img = rdhhelper.extract_main(x)


        infos = tools.decode(recover_info)
        flag = (recover_img == ori_x).all()



        new_im = Image.fromarray(recover_img.astype(np.uint8))  # np.uint8, or TypeError: Cannot handle this data type

        # new_im.show()
        new_im.save('static/imgs/recovers/result.bmp')

        return HttpResponse(str(flag) +'   ' + infos)


class extractImgView(TemplateView):
    template_name = "extractImg.html"

    def post(self, request):
        img = request.FILES.get('img')
        im_pic = Image.open(img)
        x = np.array(im_pic, dtype=np.int32)

        recover_info, recover_img = rdhhelper.extract_main(x)

        infos = tools.decode(recover_info)

        new_im = Image.fromarray(recover_img.astype(np.uint8))

        new_im.save('static/imgs/recovers/result.bmp')

        return render(request,
                      'extractShow.html',
                      context={"image_url": MEDIA_URL_PREFIX + 'recovers/result.bmp',
                                "extract_info": infos})
