from PIL import Image
import cv2

def create_watermark(image_path, final_image_path, watermark):
    # blurring
	# read image
	src = cv2.imread(image, cv2.IMREAD_UNCHANGED)
	# apply guassian blur on src image
	dst = cv2.blur(src,(7,7),cv2.BORDER_DEFAULT)
	blurred = './images/blurred.png'

	cv2.imwrite(blurred,dst)
	# end blurring
	
    main = Image.open(blurred)
    mark = Image.open(watermark)

    mask = mark.convert('L').point(lambda x: min(x, 25))
    mark.putalpha(mask)

    mark_width, mark_height = mark.size
    main_width, main_height = main.size
    aspect_ratio = mark_width / mark_height
    new_mark_width = main_width * 0.25
    mark.thumbnail((new_mark_width, new_mark_width / aspect_ratio), Image.ANTIALIAS)

    tmp_img = Image.new('RGB', main.size)

    for i in range(0, tmp_img.size[0], mark.size[0]):
        for j in range(0, tmp_img.size[1], mark.size[1]):
            main.paste(mark, (i, j), mark)
            main.thumbnail((8000, 8000), Image.ANTIALIAS)
            main.save(final_image_path, quality=100)


if __name__ == '__main__':
    create_watermark('./images/original.jpg',
                     './images/original_final_watermarked.jpg',
                     './images/logo.png')