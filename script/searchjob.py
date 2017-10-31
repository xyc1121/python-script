'''
爬虫提取51招聘信息。
'''
import sys
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup
from openpyxl import Workbook

def open51(url,keys):
	# 爬出工具
	driver = webdriver.PhantomJS(executable_path='F:\\git-source\\team\\python-script\\phantomjs\\bin\\phantomjs.exe')
	driver.get(url)
	print("进入...." + driver.title)

	elemtxtkw = driver.find_element_by_id("kwdselectid")
	
	elemtxtkw.clear()
	elemtxtkw.send_keys(keys)

	elembtnsearch = driver.find_element_by_class_name("p_but")
	elembtnsearch.click()

	#driver.close()

	for handle in driver.window_handles:
		driver.switch_to_window(handle)
	print("进入...." + driver.title)
	time.sleep(2)
	return driver

def searchJob(driver):
	#获取当前页所有的工作信息
	data = driver.page_source
	content = BeautifulSoup(data, 'lxml')
	position = content.find_all("p", {"class":"t1"}) #职位
	company = content.find_all("span", {"class":"t2"}) #公司
	location = content.find_all("span", {"class":"t3"}) #工作地点
	salary = content.find_all("span", {"class":"t4"}) #薪金
	publishdate = content.find_all("span", {"class":"t5"}) #发布时间
	info_list = []
	i = 1
	for each in position:
		info = []
		info.append(each.a.get("title"))
		info.append(each.a.get("href"))
		info.append(company[i].string)
		info.append(location[i].string)
		info.append(salary[i].string)
		info.append(publishdate[i].string)
		info_list.append(info)
		i = i + 1

	return info_list 

#切换到下一页
def nextPage(driver):
	try:
		page_num = driver.find_element_by_link_text("下一页")
		page_num.click()
	except NoSuchElementException:
		print("搜索完毕")
		flag = 0
		return flag

def main():
	url = "http://www.51job.com/hangzhou"
	keys = input("请输入搜索关键词:")
	print("请稍等片刻....")
	num = 1 
	driver = open51(url,keys)
	info_result = []
	while True:
		if num > 31:
			break
		info = searchJob(driver)
		info_result = info_result + info
		flag = nextPage(driver)
		if flag == 0:
			break
		num = num + 1
	driver.close()
	wb = Workbook()
	ws1 = wb.active
	ws1.title = "Job"
	for row in info_result:
		ws1.append(row)
	wb.save('职位信息.xlsx')

if __name__ == '__main__':
	main()

