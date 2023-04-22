import piexif
from PIL import Image as IMG
from PIL.PngImagePlugin import PngInfo
from pydantic import BaseModel
import mimetypes

mimetypes.init()


class MediaInfo(BaseModel):
    category: str
    subcategory: str


def get_media_info(filename):
    mimestart = mimetypes.guess_type(filename)[0]
    if mimestart != None:
        category, subcategory = mimestart.split('/')
    else:
        category = 'unknown'
        subcategory = 'unknown'
    return MediaInfo(category=category, subcategory=subcategory)


def set_png_tag(filename, tag):
    pnginfo = PngInfo()
    pnginfo.add_text("Comment", tag)
    im = IMG.open(filename)
    im.save(filename, pnginfo=pnginfo)


def set_jpeg_tag(filename, tag):
    exif_ifd = {
        piexif.ExifIFD.UserComment: tag.encode('utf-8')
    }
    exif_dict = {"Exif": exif_ifd}
    exif_bytes = piexif.dump(exif_dict)
    im = IMG.open(filename)
    im.save(filename, exif=exif_bytes)
        

def set_image_tag(filename, tag):
    media_info = get_media_info(filename)
    if media_info.category == 'image':
        if media_info.subcategory == 'png':
            set_png_tag(filename, tag)
        elif media_info.subcategory == 'jpeg':
            set_jpeg_tag(filename, tag)
        else:
            print("Unknown image type")
    else:
        print("Not an image")


def get_png_tag(filename):
    im = IMG.open(filename)
    pnginfo = im.info.get('Comment')
    return pnginfo


def get_jpeg_tag(filename):
    exif_dict = piexif.load(filename)
    if piexif.ExifIFD.UserComment in exif_dict['Exif']:
        return exif_dict['Exif'][piexif.ExifIFD.UserComment].decode('utf-8').strip(
            ' \t\r\n\0'
        )
    else:
        return ''


def get_image_tag(filename):
    media_info = get_media_info(filename)
    if media_info.category == 'image':
        if media_info.subcategory == 'png':
            message = get_png_tag(filename)
        elif media_info.subcategory == 'jpeg':
            message = get_jpeg_tag(filename)
        else:
            message = "Unknown image type"
    else:
        message = "Not an image"

    return message


