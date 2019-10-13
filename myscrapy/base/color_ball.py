#!/usr/bin/env python3
# -*- coding=utf-8 -*-

import random
import time

class Color_Ball(object):
	"""
	ball_num 定义了双色球的颜色和数值属性；winning_num 定义了一个得到双色球中奖号码的方法
	"""

	def ball_num(self, color):
		self.color = color
		if self.color == "red":
			num = random.randint(1, 34)
			self.num = num
		elif self.color == "blue":
			num = random.randint(1,17)
			self.num = num
		else:
			print("ball color isn't exist...")
			exit(1)
		return self.num

	def winning_num(self):
		self.winning_num = []
		for i in range(6):
			self.winning_num.append(self.ball_num("red"))
		self.winning_num.append(self.ball_num("blue"))
		return self.winning_num

	

if __name__ == "__main__":
	ball = Color_Ball()
	record_num = ball.winning_num()
	time_data = time.strftime("%Y/%m/%d %H:%M:%S", time.localtime())
	try:
		file_obj = open("color_ball_record.txt", 'a+')
	except Exception as err:
		print(err)
	file_obj.write("%02d %02d %02d %02d %02d %02d %02d %s\n" % (record_num[0], \
				record_num[1], record_num[2], record_num[3], record_num[4], record_num[5], \
					record_num[6], time_data))

	file_obj.close()
	
