import cv2

import glob



files = glob.glob("AnnotationFolder/*.txt")





for fle in files:



    # open the file and then call .read() to get the text

    with open(fle) as f:



        img = fle.split("\\")

        img = img[1].split(".")

        img = 'TestImages\\'+ img[0] + '.jpg'

        image = cv2.imread(img)

        for line in f.readlines():

            print(line)


            line = line.split(',')



            classType = line[0]

            xmin = int(line[1])

            ymin = int(line[2])

            xmax = xmin + int(line[3])

            ymax = ymin + int(line[4])



            image = cv2.rectangle(image, (xmin,ymin), (xmax, ymax), (0, 255, 255), 3)



cv2.imwrite("cars.jpg", image)

cv2.waitKey(0)
