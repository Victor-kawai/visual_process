'''
Author: Victor-kawai 1900017878@pku.edu.cn
Date: 2024-04-11 18:31:28
LastEditors: Victor-kawai 1900017878@pku.edu.cn
LastEditTime: 2024-05-22 11:47:09
FilePath: \毕设\code\ocr_api.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
import requests
import json
import os

# 本地文件
def ocr_space_file(filename, overlay=False, api_key='K82023489588957', language='chs'):
    """ OCR.space API request with local file.
        Python3.5 - not tested on 2.7
    :param filename: Your file path & name.
    :param overlay: Is OCR.space overlay required in your response.
                    Defaults to False.
    :param api_key: OCR.space API key.
                    Defaults to 'helloworld'.
    :param language: Language code to be used in OCR.
                    List of available language codes can be found on https://ocr.space/OCRAPI
                    Defaults to 'en'.
    :return: Result in JSON format.
    """

    payload = {'isOverlayRequired': overlay,
               'apikey': api_key,
               'language': language,
               'detectOrientation': 'true',
               'scale': 'true',
               'OCREngine': 2,
               }
    with open(filename, 'rb') as f:
        r = requests.post('https://api.ocr.space/parse/image',
                          files={filename: f},
                          data=payload,
                          )
    test_file = r.content.decode()
    print(json.loads(test_file))
    txt = json.loads(test_file)['ParsedResults'][0]['ParsedText']
    print(txt)
    return txt


# 远程文件
def ocr_space_url(url, overlay=False, api_key='helloworld', language='chs'):
    """ OCR.space API request with remote file.
        Python3.5 - not tested on 2.7
    :param url: Image url.
    :param overlay: Is OCR.space overlay required in your response.
                    Defaults to False.
    :param api_key: OCR.space API key.
                    Defaults to 'helloworld'.
    :param language: Language code to be used in OCR.
                    List of available language codes can be found on https://ocr.space/OCRAPI
                    Defaults to 'en'.
    :return: Result in JSON format.
    """

    payload = {'url': url,
               'isOverlayRequired': overlay,
               'apikey': api_key,
               'language': language,
               }
    r = requests.post('https://api.ocr.space/parse/image',
                      data=payload,
                      )
    return r.content.decode()

def ocr_request(organization):
    print("==== ocr识别开始 ====")
    path = "元丰新制/"+organization+"/切分后"+organization
    target_file_name = "元丰新制/"+organization+"/"+organization+"文本.md"
    files = os.listdir(path)
    f = open(target_file_name, "w", encoding="utf-8")
    i = 0
    for file in files:
            f.write("## /page{"+file[0:file.rfind(".")]+"}")
            print(file)
            f.write("\n")
            text = ocr_space_file(filename=path+'/'+file, language='chs')
            #print(text)
            f.write(text)
            f.write("\n")
            i += 1
    f.close()
    print("==== ocr识别结束 ====")
    return target_file_name

if __name__ == "__main__":
    organization = "宰执官类"
    ocr_request(organization)