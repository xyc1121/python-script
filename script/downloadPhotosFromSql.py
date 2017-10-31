'''
sql来源，下载照片。
'''
#! /usr/bin/python
# coding = utf-8
import pymysql.cursors
import os
import urllib.request

# 数据库连接
con = pymysql.connect(host = '127.0.0.1',
	port = 3306,
	user = '***',
	password = '******',
	db = 'app_yo',
	charset = 'utf8'
	)

def main():
	row = getPhotos()
	for i in row:
		# 下载后的保存文件夹
		albumname = 'E:\\downloadPhotos\\' + i[0]
		# 图片网络url
		url = i[1]
		# 图片文件名
		filename = i[2]
		# 下载后的保存地址
		file = albumname + '\\' + filename
		
		# 若保存文件夹不存在，则新建文件夹
		if not os.path.exists(albumname) :
			os.makedirs(albumname)
		# 下载图片，保存在指定地址
		urllib.request.urlretrieve(url, file)
		print(url + " download ok!")
	con.close()


# 获取照片
def getPhotos():
	try:
		sql = ' SELECT \
				  c.`name` as albumname,\
				  d.`url`, \
				  d.`filename` \
				FROM\
				  app_yo.`yo_clubalbums` a \
				  INNER JOIN app_yo.`yo_photos` b \
				    ON a.`albumid` = b.`albumid` \
				  LEFT JOIN app_yo.`yo_albums` c \
				    ON a.`albumid` = c.`id` \
				  LEFT JOIN svr_file.`files_0` d \
				    ON b.`fid` = d.`id` \
				WHERE a.`schoolid` = 865;'
		cursor = con.cursor()
		cursor.execute(sql)
		row = cursor.fetchall()
		return row
	except Exception:
		print('getPhotos error')
	finally:
		cursor.close()

if __name__ == '__main__':
	main()