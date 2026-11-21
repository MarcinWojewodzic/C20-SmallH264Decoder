import requests,re,pathlib,concurrent.futures
urls=['https://www.lcsc.com/product-detail/C46898862.html','https://www.mouser.cn/ProductDetail/STMicroelectronics/LSM6DSV80XTR']
def run(u):
 try:
  r=requests.get(u,timeout=15);print(u,r.status_code);print('\n'.join(set(re.findall(r'https?[^\s"<>]+(?:pdf|PDF)[^\s"<>]*',r.text))))
 except Exception as e:print(type(e).__name__)
list(concurrent.futures.ThreadPoolExecutor().map(run,urls))
