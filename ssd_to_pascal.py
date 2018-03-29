from detector import Detector
from pascal_writer import PascalWriter
from PIL import Image, ImageDraw

gpu_id = 0
model_def = ""
model_weight = ""
image_resize = 300
labelmap_file = ""
image_file = ""
image_dir = ""

def main():
    detector = Detector(gpu_id,
                        model_def, model_weights,
                        image_resize, labelmap_file)
    result = detector.detect(image_file)
    print(result)

    img = Image.open(image_file)
    draw = ImageDraw.Draw(img)
    width, height = img.size

    writer = PascalWriter(image_dir, image_file, img.size)
    for item in result:
        xmin, ymin, xmax, ymax = item[0], item[1], item[2], item[3]
        name = item[-1]
        draw.rectangle([xmin, ymin, xmax, ymax], outline=(255, 0, 0))
        draw.text([xmin, ymin], item[-1] + str(item[-2]), (0, 0, 255))
        writer.add_bbox(xmin, ymin, xmax , ymax, name)
    writer.save()
    img.save('detect_result.jpg')

if __name__ == "__main__":
    main()
