import cv2, random, math
import numpy as np

def getDistance(point1, point2):
    x = point2[0] - point1[0]
    x *= x
    y = point2[1] - point1[1]
    y *= y
    distance = math.sqrt(x + y)
    return(distance)

def poissonDistribution(minDist, numPoints, shape):
    points = []
    while (len(points) < numPoints):
        newPoint = ([random.randint(0, shape[1] - 1), random.randint(0, shape[0])])
        distanceSatisfied = True
        for point in points:
            if (getDistance(newPoint, point) < minDist):
                distanceSatisfied = False
                break
        if (distanceSatisfied):
            points.append(newPoint)
    return (points)

def generateColors(numColors, variation = -1):
    if (variation == -1):
        variation = numColors

    colors = []
    for i in range(variation):
        colors.append([random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)])

    while(len(colors) < numColors):
        for i in range(variation):
            if (len(colors) < numColors):
                colors.append(colors[i])
    return(colors)

def getLosest(values):
    lowest = values[0]
    index = 0
    for i in range(1, len(values)):
        if (values[i] < lowest):
            lowest = values[i]
            index = i
    return(index)

def generateVectors(numVectors, lowerBounds = [-1.5, -1.5, -0.5], upperBounds = [1.5, 1.5, 0.5]):
    vectors = []
    for i in range(numVectors):
        vectors.append([])
        for j in range(3):
            vectors[i].append(random.uniform(lowerBounds[j], upperBounds[j]))

    return (vectors)

def applyVectors(points, vectors, shape, vectorBounds = [-3, 3]):
    for i in range(len(points)):
        points[i][0] += vectors[i][0]
        points[i][1] += vectors[i][1]
        vectors[i][0] += vectors[i][2]
        vectors[i][1] += vectors[i][2]
        if ((vectors[i][0] < vectorBounds[0] or vectors[i][1] < vectorBounds[0]) and vectors[i][2] < 0):
            vectors[i][2] *= -1
        elif((vectors[i][0] > vectorBounds[1] or vectors[i][1] > vectorBounds[1]) and vectors[i][2] > 0):
            vectors[i][2] *= -1


def colorImage(img, points, pointColors, divisor = 500):
    for y in range(img.shape[0]):
        for x in range(img.shape[1]):
            distances = []
            point1 = [y, x]
            for i in range(len(points)):
                point2 = points[i]
                distances.append(getDistance(point1, point2))
            previous = distances.copy()
            index = getLosest(distances)
            distance = distances[index]
            multiplier = distance / divisor
            if (multiplier == 0):
                multiplier = 0.01
            newColor = pointColors[index].copy()
            for i in range(3):
                # pixelColor = int(newColor[i] / multiplier)
                pixelColor = newColor[i] * multiplier
                # pixelColor = newColor[i] - (newColor[i] * multiplier)
                if (pixelColor < 0):
                    newColor[i] = 0
                if (pixelColor > 255):
                    newColor[i] = 255
                else:
                    newColor[i] = pixelColor

            img[y, x] = newColor

img = np.zeros([1000, 1000, 3], np.uint8)

numPoints = 50

points = poissonDistribution(100, numPoints, img.shape[:2])
pointColors = generateColors(numPoints)
vectors = generateVectors(numPoints)

height, width, layers = img.shape
size = (width,height)
fourcc = cv2.VideoWriter_fourcc(*'H264')
out = cv2.VideoWriter('voronoise.mp4',fourcc, 24, size)

for i in range(1000):
    print(i)
    colorImage(img, points, pointColors, 500)
    applyVectors(points, vectors, img.shape[:2])
    out.write(img)
    cv2.imshow("Img", img)
    cv2.waitKey(1)

out.release()
