from io import BytesIO

from PIL import Image, ImageDraw, ImageFont
from django.core.files.storage import FileSystemStorage
from django.core.files.uploadedfile import InMemoryUploadedFile


class WatermarkStroage(FileSystemStorage):
    def save(self, name, content, max_length=None):#重写上传文件的save方法
        if 'image' in content.content_type:#判断正文中是否含有图片
            image=self.watermark_with_text(content,'Haiii','red')#加水印
            content=self.convert_image_to_file(image,name)
        return super().save(name,content,max_length=max_length)

    def convert_image_to_file(self,image,name):#把打上水印的image对象转换成文件对象，即BytesIO对象
        temp=BytesIO()
        image.save(temp,format='PNG')
        file_size=temp.tell()
        return InMemoryUploadedFile(temp,None,name,'image/png',file_size,None)

    def watermark_with_text(self,file_obj,text,color,fontfamily=None):
        image=Image.open(file_obj).convert('RGBA')#把传递的文件对象转换成image对象并把格式转为RGBA
        draw=ImageDraw.Draw(image)
        width,height=image.size
        margin=10
        if fontfamily:
            font=ImageFont.truetype(fontfamily,int(height/20))
        else:
            font=None
        textWidth,textHeight=draw.textsize(text,font)
        x=(width-textWidth-margin)/2
        y=height-textHeight-margin
        draw.text((x,y),text,color,font)
        return image