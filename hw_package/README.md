Short description: 
This is console utility for getting random image from duckduckgo by keyword and convert it into ascii-art file.

How to use:
	Console app:
		python3 ddg_image.py --keyword=<image_request_keyword>

	Module:
		import ddg_image

		ddg_images_obj = ddg_image("<keyword>")
		ddg_images_obj.set_random_picture_index()
		ddg_images_obj.picture_to_ascii()



What tou get:
	three files: 
	  * file with random image from duckduckgo
	  * file with image converted into ascii-art
	  * log file