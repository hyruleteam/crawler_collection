import os
import urllib.request

def save_img(file_path='/Users/wenyu/Desktop/weather'):
    #保存图片到磁盘文件夹 file_path中，默认为当前脚本运行目录下的 book\img文件夹
    try:
        if not os.path.exists(file_path):
            print ('文件夹',file_path,'不存在，重新建立')
            #os.mkdir(file_path)
            os.makedirs(file_path)
        for i in range(0,33):
        	if i < 10:
        		new_name = '0'+str(i)
        	else:
        		new_name = str(i)

        	print(new_name)
        	img_url = 'https://mat1.gtimg.com/pingjs/ext2020/weather/pc/icon/weather/day/'+new_name+'.png'
        	#获得图片后缀
	        file_suffix = os.path.splitext(img_url)[1]
	        #拼接图片名（包含路径）
	        filename = '{}{}{}{}'.format(file_path,os.sep,new_name,file_suffix)
	       #下载图片，并保存到文件夹中
	        urllib.request.urlretrieve(img_url,filename=filename)
    except IOError as e:
        print ('文件操作失败',e)
    except Exception as e:
        print ('错误 ：',e)



if __name__ == '__main__':
    save_img()