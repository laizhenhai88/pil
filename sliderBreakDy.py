# coding=utf-8

import os,shutil
from sys import argv
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageColor
import math

DEBUG = True
def log(*args):
    if DEBUG:
        print(*args)

def readDataPixel(data, point):
    return data[point[1]*data.size[0]+point[0]]

def interference_line(image):
    data = image.getdata()
    draw = ImageDraw.Draw(image)
    for x in range(1,image.size[0] - 1):
        for y in range(1,image.size[1] - 1):
            if readDataPixel(data,(x,y)) == 255:
                continue
            count = 0
            if readDataPixel(data,(x,y-1)) == 255:
                count = count + 1
            if readDataPixel(data,(x,y+1)) == 255:
                count = count + 1
            if readDataPixel(data,(x-1,y)) == 255:
                count = count + 1
            if readDataPixel(data,(x+1,y)) == 255:
                count += 1
            if count > 2:
                draw.point((x,y),255)


def convert_0_1_reverse(image, limit):
    data = image.getdata()
    draw = ImageDraw.Draw(image)
    for x in range(0,image.size[0]):
        for y in range(0,image.size[1]):
            if readDataPixel(data,(x,y)) < limit:
                draw.point((x,y),255)
            else:
                draw.point((x,y),0)

def convert_0_1_reverse2(image, limit1, limit2):
    data = image.getdata()
    draw = ImageDraw.Draw(image)
    for x in range(0,image.size[0]):
        for y in range(0,image.size[1]):
            if limit1 <= readDataPixel(data,(x,y)) and readDataPixel(data,(x,y)) <= limit2:
                draw.point((x,y),0)
            else:
                draw.point((x,y),255)

def find_near_all(find_p, distance):
    p = []
    nearest = 30
    for i in range(0, len(find_p) -1):
        for j in range(i+1, len(find_p)):
            near1 = abs(abs(find_p[j] - find_p[i]) - distance)
            if near1 < nearest:
                p.append([find_p[i], find_p[j]])
    return p

def find_near_all2(find_p, distance):
    p1 = []
    p2 = []
    nearest = 10
    for i in range(0, len(find_p) -1):
        for j in range(i+1, len(find_p)):
            # 写死,特殊情况
            near1 = abs(abs(find_p[j] - find_p[i]) - 100)
            if near1 < nearest:
                p1.append([find_p[i], find_p[j]])

            near2 = abs(abs(find_p[j] - find_p[i]) - 140)
            if near2 < nearest:
                p2.append([find_p[i], find_p[j]])
    log('len p1 p2', len(p1), len(p2))
    if len(p1) > len(p2) * 3:
        return p1
    else:
        return p2

def histogram_ori(image, min_value):
    hx = [0] * image.size[0]
    hy = [0] * image.size[1]
    for x in range(0,image.size[0]):
        for y in range(0,image.size[1]):
            if image.getpixel((x,y)) == 0:
                hx[x] += 1
                hy[y] += 1

    # hx.sort()
    # hy.sort()
    # log(hx)
    # log(hy)
    log('max hx:', max(hx[1:-1]))
    log('max hy:', max(hy[1:-1]))
    px = []
    py = []
    for x in range(1, image.size[0]-1):
        if hx[x] >= min_value:
            px.append(x)
    for y in range(1, image.size[1]-1):
        if hy[y] >= min_value:
            py.append(y)
    return [px,py]

def histogram(image, min_value):
    hx = [0] * image.size[0]
    hy = [0] * image.size[1]
    hx_count = 0
    hy_count = [0] * image.size[1]
    for x in range(0,image.size[0]):
        for y in range(0,image.size[1]):
            if image.getpixel((x,y)) == 0:
                hx_count += 1
                hy_count[y] += 1
            else:
                if hx_count >= min_value:
                    hx[x] += hx_count
                if hy_count[y] >= min_value:
                    hy[y] += hy_count[y]
                hx_count = 0
                hy_count[y] = 0


    # hx.sort()
    # hy.sort()
    # log(hx)
    # log(hy)
    log('max hx:', max(hx[1:-1]))
    log('max hy:', max(hy[1:-1]))
    px = []
    py = []
    for x in range(1, image.size[0]-1):
        if hx[x] >= min_value:
            px.append(x)
    for y in range(1, image.size[1]-1):
        if hy[y] >= min_value:
            py.append(y)
    return [px,py]

def find_all_pair(image, pair_x, pair_y):
    all_pair = []
    for px in pair_x:
        for py in pair_y:
            sum = 0
            for x in range(px[0], px[1]):
                if image.getpixel((x,py[0])) == 0:
                    sum += 1
                if image.getpixel((x,py[1])) == 0:
                    sum += 1
            for y in range(py[0], py[1]):
                if image.getpixel((px[0],y)) == 0:
                    sum += 1
                if image.getpixel((px[1],y)) == 0:
                    sum += 1
            all_pair.append([px,py,sum])

    return sorted(all_pair, key=lambda p:-p[2])























def sliderBreak(file):
    dir = os.path.basename(file)
    im = Image.open(file)

    # no resize
    try:
        # 把第一个块的图片切出来,转换成灰度图
        leftIm = im.crop((0,0,180,im.size[1])).convert('L')
        # 根据阈值把白色块边框过滤出来
        convert_0_1_reverse(leftIm, 200)
    except Exception as e:
        print('failed, image read error')
        return -1
    # 去躁点
    interference_line(leftIm)
    # 算轮廓
    leftIm = leftIm.filter(ImageFilter.CONTOUR)

    if DEBUG:
        os.mkdir('dist/' + dir)
        leftIm.save('dist/' + dir + '/leftIm.png')

    # 根据阈值过滤直方图,得到阈值大的坐标
    min_ht_value = 10
    ht = histogram(leftIm, min_ht_value)
    if len(ht[0]) + len(ht[1]) < 2:
        ht = histogram(leftIm, 20)
        if len(ht[0]) + len(ht[1]) < 2:
            print('failed', 'ht:', ht)
            return -1

    if len(ht[0]) == 0:
        print('failed temp, ht x is 0, maybe need default')
        return -1

    if len(ht[1]) == 0:
        ht = histogram(leftIm, 20)
        if len(ht[1]) == 0:
            print('failed temp, ht y is 0, maybe need all')
            return -1

    # 找到双边配对的坐标
    block_size = 120
    pair_x = find_near_all(ht[0], block_size)
    # if len(pair_x) == 0:
    #     # 没有找到配对,则构造虚拟配对
    #     temp = []
    #     for i in ht[0]:
    #         temp.append(i)
    #         # 给可能的边配上对边,应对出现单边模糊的情况
    #         if i + block_size < leftIm.size[0] -1:
    #             temp.append(i+block_size)
    #         if i - block_size > 0:
    #             temp.append(i-block_size)
    #         ht[0] = list(set(temp))
    #         ht[0].sort()
    #         pair_x = find_near_all(ht[0], block_size)


    if len(pair_x) == 0:
        print('failed, no pair x')
        return -1


    pair_y = find_near_all(ht[1], block_size)
    # if len(pair_y) == 0:
    #     temp = []
    #     for i in ht[1]:
    #         temp.append(i)
    #         if i + block_size < leftIm.size[1] -1:
    #             temp.append(i+block_size)
    #         if i - block_size > 0:
    #             temp.append(i-block_size)
    #         ht[1] = list(set(temp))
    #         ht[1].sort()
    #         pair_y = find_near_all(ht[1], block_size)

    if len(pair_y) == 0:
        print('failed, no pair y')
        return -1

    # 计算四边的阈值并排序
    log('len pair x,y:',len(pair_x), len(pair_y))
    all_pair_left = find_all_pair(leftIm, pair_x, pair_y)
    log('all_pair_left:', all_pair_left)

    x1 = all_pair_left[0][0][0]
    x2 = all_pair_left[0][0][1]
    y1 = all_pair_left[0][1][0]
    y2 = all_pair_left[0][1][1]









    block_size = math.floor((x2-x1+y2-y1)/2)
    log('block_size:', block_size)
    # here is right image
    rightIm = im.crop((180, y1-20, im.size[0], y2+20)).convert('L')
    convert_0_1_reverse2(rightIm, 0, 130)
    rightIm = rightIm.filter(ImageFilter.CONTOUR)
    interference_line(rightIm)

    if DEBUG:
        rightIm.save('dist/' + dir + '/rightIm.png')

    ht = histogram(rightIm, min_ht_value)
    if len(ht[0]) + len(ht[1]) < 2:
        ht = histogram(rightIm, 20)
        if len(ht[0]) + len(ht[1]) < 2:
            print('failed right', 'ht:', ht)
            return -1

    if len(ht[0]) == 0:
        ht = histogram(rightIm, 20)
        if len(ht[0]) == 0:
            print('failed right temp, ht x is 0, maybe need all')
            return -1

    if len(ht[1]) == 0:
        print('failed right temp, ht y is 0, maybe need origin')
        return -1

    pair_x = find_near_all(ht[0], block_size)
    if len(pair_x) == 0:
        temp = []
        for i in ht[0]:
            temp.append(i)
            if i + block_size < rightIm.size[0] -1:
                temp.append(i+block_size)
            if i - block_size > 0:
                temp.append(i-block_size)
            ht[0] = list(set(temp))
            ht[0].sort()
            pair_x = find_near_all(ht[0], block_size)
            if len(pair_x) > 100:
                print('failed, too many pair x2')
                return -1

    if len(pair_x) == 0:
        print('failed, no pair x2')
        return -1

    pair_y = find_near_all(ht[1], block_size)
    if len(pair_y) == 0:
        temp = []
        for i in ht[1]:
            temp.append(i)
            if i + block_size < rightIm.size[1] -1:
                temp.append(i+block_size)
            if i - block_size > 0:
                temp.append(i-block_size)
            ht[1] = list(set(temp))
            ht[1].sort()
            pair_y = find_near_all(ht[1], block_size)
            if len(pair_y) > 100:
                print('failed, too many pair y2')
                return -1

    if len(pair_y) == 0:
        print('failed, no pair y2')
        return -1

    log('len pair x,y:',len(pair_x), len(pair_y))
    all_pair_right = find_all_pair(rightIm, pair_x, pair_y)
    log('all_pair_right', all_pair_right)
    all_pair_right_len = max(min(int(len(all_pair_right)*1/3), 6), 2)
    all_pair_right = all_pair_right[0:all_pair_right_len]
    log(all_pair_right)

    # avg
    sum = 0
    for pair in all_pair_right:
        sum += pair[2]
    avg = int(sum/len(all_pair_right)*4/5)

    sum = 0
    count = 0
    for pair in all_pair_right:
        if pair[2] > avg:
            count += 1
            sum = sum + pair[0][0] + pair[0][1]

    x = int(sum / count / 2)
    x21 = math.floor(x - block_size/2 + 180)
    x22 = math.floor(x + block_size/2 + 180)
    distance = math.floor(x - block_size/2 + 180 - x1)

    log('x21,x22:', x21,x22)
    print(distance)

    draw = ImageDraw.Draw(im)
    draw.line([(x1,y1),(x2,y1),(x2,y2),(x1,y2),(x1,y1)], 'blue', 2)
    draw.line([(x21,y1),(x22,y1),(x22,y2),(x21,y2),(x21,y1)], 'blue', 2)

    if DEBUG:
        im.save('dist/'+os.path.basename(file + '.jpg'))

    return distance

def main():
    if len(argv) != 2:
        print('参数不对')
        return
    sliderBreak(argv[1])

if __name__ == "__main__":
    DEBUG = False
    main()
