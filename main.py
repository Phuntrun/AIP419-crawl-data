import extract_dish_link, extract_recipe, convert_link, mutil_thread_download_image
import asyncio

CLASS1 = ['thịt bò', 'bún', 'rau muống', 'giá đỗ', 'chanh', 'bánh phở', 'xương bò',
    'gân bò', 'húng quế', 'ngò gai']
CLASS2 = ['hành tây', 'quế', 'hoa hồi', 'thịt heo',
    'trứng', 'cà chua', 'dưa chua', 'thịt bằm', 'đậu hũ']
CLASS3 = ['rau sống', 'mắm tôm', 'chanh dây', 'xúc xích', 'mì tôm', 'thịt gà',
    'nấm', 'nấm rơm', 'bắp cải', 'cá trê']
CLASS4 = ['cà rốt', 'khoai tây', 'khoai lang',
    'đậu que', 'bông cải', 'bí đỏ', 'bí đao', 'mướp', 'rau ngót', 'mồng tơi']
CLASS5 = ['thịt vịt', 'bắp', 'bơ', 'dưa leo', 'dứa', 'cần tây', 'mực', 'tôm',
    'cá hồi', 'cá thu']
CLASS6 = ['cá lóc', 'cá riêu', 'thịt nai', 'lươn','bò viên', 'bánh mì', 'gạo', 
          'bắp non', 'đậu xanh','đậu đỏ', 'đậu nành']

# asyncio.run(extract_dish_link.extract(CLASS2, "csv/dish_link2.csv"))
# print("extracted dish link succeed!")
# asyncio.run(extract_recipe.extract(filename_input="csv/dish_link2.csv",filename_output="csv/img_page_link2.csv"))
# print("extracted recipe link succeed!")
# asyncio.run(convert_link.convert(filename_input="csv/img_page_link2.csv",filename_output="csv/img_link2.csv"))
# print("convert completely!")
mutil_thread_download_image.download(filename_input="csv/img_link2.csv")
print("download completely!")

# asyncio.run(extract_dish_link.extract(CLASS3, "csv/dish_link3.csv"))
# print("extracted dish link succeed!")
# asyncio.run(extract_recipe.extract(filename_input="csv/dish_link3.csv",filename_output="csv/img_page_link3.csv"))
# print("extracted recipe link succeed!")
# asyncio.run(convert_link.convert(filename_input="csv/img_page_link3.csv",filename_output="csv/img_link3.csv"))
# print("convert completely!")

# asyncio.run(extract_dish_link.extract(CLASS4, "csv/dish_link4.csv"))
# print("extracted dish link succeed!")
# asyncio.run(extract_recipe.extract(filename_input="csv/dish_link4.csv",filename_output="csv/img_page_link4.csv"))
# print("extracted recipe link succeed!")
# asyncio.run(convert_link.convert(filename_input="csv/img_page_link4.csv",filename_output="csv/img_link4.csv"))
# print("convert completely!")

# asyncio.run(extract_dish_link.extract(CLASS5, "csv/dish_link5.csv"))
# print("extracted dish link succeed!")
# asyncio.run(extract_recipe.extract(filename_input="csv/dish_link5.csv",filename_output="csv/img_page_link5.csv"))
# print("extracted recipe link succeed!")
# asyncio.run(convert_link.convert(filename_input="csv/img_page_link5.csv",filename_output="csv/img_link5.csv"))
# print("convert completely!")

# asyncio.run(extract_dish_link.extract(CLASS6, "csv/dish_link6.csv"))
# print("extracted dish link succeed!")
# asyncio.run(extract_recipe.extract(filename_input="csv/dish_link6.csv",filename_output="csv/img_page_link6.csv"))
# print("extracted recipe link succeed!")
# asyncio.run(convert_link.convert(filename_input="csv/img_page_link6.csv",filename_output="csv/img_link6.csv"))
# print("convert completely!")
