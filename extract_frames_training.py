import cv2
import os
import zipfile
import shutil
# 第一步：创建文件夹
if not os.path.exists('./images_training/'):
    os.makedirs('./images_training/')

if not os.path.exists('./preview_images_training/'):
    os.makedirs('./preview_images_training/')
# 第二步：读取视频并切分
vc = cv2.VideoCapture('./src/video_training.mov')

# 查看视频 fps
fps = vc.get(cv2.CAP_PROP_FPS)
print('视频FPS =', fps)

i = 0
save_id = 0
rval = True
# 每 7 帧保存 1 张
interval = 7

while True:
    if (i + 1) % 100 == 0:
        print(i + 1)

    rval, frame = vc.read()

    if rval == True:
        if (i + 1) % interval == 0:
            cv2.imwrite('./images_training/{:04d}.jpg'.format(save_id + 1), frame)
            save_id = save_id + 1

        i = i + 1
        cv2.waitKey(1)
    else:
        break

vc.release()

# 第三步：查看输出结果
l = os.listdir('./images_training/')
print('共切分出 {} 张图片'.format(len(l)))

# 第四步：压缩 images 文件夹
zf = zipfile.ZipFile('images_training.zip', 'w', zipfile.ZIP_DEFLATED)

for file_name in os.listdir('./images_training/'):
    file_path = './images_training/' + file_name
    zf.write(file_path, arcname=file_name)

zf.close()

print('images_training.zip 压缩完成')

# 第五步：预留展示图片
files = sorted(os.listdir('./images_training/'))
preview_num = 20
n = len(files)

for k in range(preview_num):
    idx = round(k * (n - 1) / (preview_num - 1))
    src = './images_training/' + files[idx]
    dst = './preview_images_training/' + files[idx]
    shutil.copy(src, dst)

print('preview_images_training 中共保留 {} 张图片'.format(len(os.listdir('./preview_images_training/'))))