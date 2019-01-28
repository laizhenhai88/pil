# coding=utf-8

import os,shutil
from sys import argv
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageColor

DEBUG = False
def log(*args):
    if DEBUG:
        print(*args)

def interference_line(image):
    imageCopy = image.copy()
    draw = ImageDraw.Draw(image)
    for x in range(1,image.size[0] - 1):
        for y in range(1,image.size[1] - 1):
            if imageCopy.getpixel((x,y)) == 255:
                continue
            count = 0
            if imageCopy.getpixel((x,y-1)) == 255:
                count = count + 1
            if imageCopy.getpixel((x,y+1)) == 255:
                count = count + 1
            if imageCopy.getpixel((x-1,y)) == 255:
                count = count + 1
            if imageCopy.getpixel((x+1,y)) == 255:
                count += 1
            if count > 2:
                draw.point((x,y),255)


def find_near_all(find_p, distance):
    p = []
    nearest = 10
    for i in range(0, len(find_p) -1):
        for j in range(i+1, len(find_p)):
            near = abs(abs(find_p[j] - find_p[i]) - distance)
            if near < nearest:
                p.append([find_p[i], find_p[j]])
    return p

def histogram(image, min_value):
    hx = [0] * image.size[0]
    hy = [0] * image.size[1]
    for x in range(0,image.size[0]):
        for y in range(0,image.size[1]):
            if image.getpixel((x,y)) == 0:
                hx[x] += 1
                hy[y] += 1
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
        leftIm = im.crop((0,0,390-190,1220-480)).filter(ImageFilter.CONTOUR).convert('1')
    except Exception as e:
        print('failed, image read error')
        return -1
    interference_line(leftIm)

    if DEBUG:
        os.mkdir('dist/' + dir)
        leftIm.save('dist/' + dir + '/leftIm.png')

    min_ht_value = 60
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
        ht = histogram(leftIm, 7)
        if len(ht[1]) == 0:
            print('failed temp, ht y is 0, maybe need all')
            return -1

    block_size = 172
    # pair_x = find_near_all(ht[0], block_size)
    # if len(pair_x) == 0:
    #     # fill
    #     temp = []
    #     for i in ht[0]:
    #         temp.append(i)
    #         if i + block_size < leftIm.size[0] -1:
    #             temp.append(i+block_size)
    #         if i - block_size > 0:
    #             temp.append(i-block_size)
    #     temp.sort()
    #     ht[0] = temp
    #     pair_x = find_near_all(ht[0], block_size)


    temp = []
    for i in ht[0]:
        temp.append(i)
        if i + block_size < leftIm.size[0] -1:
            temp.append(i+block_size)
        if i - block_size > 0:
            temp.append(i-block_size)
        ht[0] = list(set(temp))
        ht[0].sort()
        pair_x = find_near_all(ht[0], block_size)

    if len(pair_x) == 0:
        print('failed, no pair x')
        return -1


    # pair_y = find_near_all(ht[1], block_size)
    # if len(pair_y) == 0:
    #     # fill
    #     temp = []
    #     for i in ht[1]:
    #         temp.append(i)
    #         if i + block_size < leftIm.size[1] -1:
    #             temp.append(i+block_size)
    #         if i - block_size > 0:
    #             temp.append(i-block_size)
    #     ht[1] = list(set(temp))
    #     ht[1].sort()
    #     pair_y = find_near_all(ht[1], block_size)

    temp = []
    for i in ht[1]:
        temp.append(i)
        if i + block_size < leftIm.size[1] -1:
            temp.append(i+block_size)
        if i - block_size > 0:
            temp.append(i-block_size)
        ht[1] = list(set(temp))
        ht[1].sort()
        pair_y = find_near_all(ht[1], block_size)

    if len(pair_y) == 0:
        print('failed, no pair y')
        return -1

    all_pair_left = find_all_pair(leftIm, pair_x, pair_y)
    log(all_pair_left)

    y1 = all_pair_left[0][1][0] + 480
    y2 = all_pair_left[0][1][1] + 480








    # here is right image
    rightIm = im.crop((423-190, y1-20-480, 1370-190, y2+20-480)).filter(ImageFilter.CONTOUR).convert('1')
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
        ht = histogram(rightIm, 7)
        if len(ht[0]) == 0:
            print('failed right temp, ht x is 0, maybe need all')
            return -1

    if len(ht[1]) == 0:
        print('failed right temp, ht y is 0, maybe need origin')
        return -1

    block_size = 172
    # pair_x = find_near_all(ht[0], block_size)
    # if len(pair_x) == 0:
    #     # fill
    #     temp = []
    #     for i in ht[0]:
    #         temp.append(i)
    #         if i + block_size < rightIm.size[0] -1:
    #             temp.append(i+block_size)
    #         if i - block_size > 0:
    #             temp.append(i-block_size)
    #     temp.sort()
    #     ht[0] = temp
    #     pair_x = find_near_all(ht[0], block_size)

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

    # pair_y = find_near_all(ht[1], block_size)
    # if len(pair_y) == 0:
    #     # fill
    #     temp = []
    #     for i in ht[1]:
    #         temp.append(i)
    #         if i + block_size < rightIm.size[1] -1:
    #             temp.append(i+block_size)
    #         if i - block_size > 0:
    #             temp.append(i-block_size)
    #     temp.sort()
    #     ht[1] = temp
    #     pair_y = find_near_all(ht[1], block_size)
    #     if len(pair_y) > 100:
    #         print('failed, too many pair y')
    #         return -1

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
            print('failed, too many pair y')
            return -1

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
    x1 = x - 86 + 423
    x2 = x + 86 + 423
    distance = x + 86 + 47

    log('y1,y2:', y1,y2)
    log('x1,x2:', x1,x2)
    print(distance)

    draw = ImageDraw.Draw(im)
    draw.line([(i[0]-190,i[1]-480) for i in [(x1,y1),(x2,y1),(x2,y2),(x1,y2),(x1,y1)]], 'blue', 4)
    draw.line([(i[0]-190,i[1]-480) for i in [(206,y1),(378,y1),(378,y2),(206,y2),(206,y1)]], 'blue', 4)

    if DEBUG:
        im.save('dist/'+os.path.basename(file + '.jpg'))
#    else:
#        im = im.resize((350,200))
#        im.save(file+'-result.jpg')

    return distance

def main():
    if len(argv) != 2:
        print('参数不对')
        return
    sliderBreak(argv[1])

if __name__ == "__main__":
    DEBUG = False
    main()
