#!/usr/bin/env python3
# -*- coding=utf-8 -*-

class Post_Office(object):
	"""
	分别定义杂志，报纸，小说的读者列表,并且定义订阅和邮寄方法
	"""
	magazine_subscriber = []
	newpaper_subscriber = []
	novel_subscriber = []

	def register(self, book_type, people):
		"""
		读者订阅不同类型的书籍
		"""
		if book_type == "magazine" and people not in self.magazine_subscriber:
			self.magazine_subscriber.append(people)
			print("【邮局】%s orders a %s" % (people.name, book_type))
		elif book_type == "newpaper" and people not in self.newpaper_subscriber:
			self.newpaper_subscriber.append(people)
			print("【邮局】%s orders a %s" % (people.name, book_type))
		elif book_type == "novel" and people not in self.novel_subscriber:
			self.novel_subscriber.append(people)
			print("【邮局】%s orders a %s" % (people.name, book_type))
		else:
			print("抱歉，您已经订阅或者订阅书籍类型不存在,当前仅售报纸、杂志、小说...")

	def cancel(self, book_type, people):
		"""
		读者取消订阅
		"""
		if book_type == "magazine" and people in self.magazine_subscriber:
			self.magazine_subscriber.remove(people)
			print("【邮局】%s cancels a %s" % (people.name, book_type))
		elif book_type == "newpaper" and people in self.newpaper_subscriber:
			self.newpaper_subscriber.remove(people)
			print("【邮局】%s cancels a %s" % (people.name, book_type))
		elif book_type == "novel" and people in self.novel_subscriber:
			self.novel_subscriber.remove(people)
			print("【邮局】%s cancels a %s" % (people.name, book_type))
		else:
			print("抱歉，您尚未订阅或者订阅书籍类型不存在,当前仅售报纸、杂志、小说...")

	def post_book(self, book_type, book_name):
		"""
		邮局根据出版社的最新发布将最新的书籍邮寄到读者手里
		"""
		if book_type == "magazine":
			for user in Post_Office.magazine_subscriber:
				user.post(book_type, book_name)
		elif book_type == "newpaper":
			for user in Post_Office.newpaper_subscriber:
				user.post(book_type, book_name)
		elif book_type == "novel":
			for user in Post_Office.novel_subscriber:
				user.post(book_type, book_name)



class Publishing_House(Post_Office):
	"""
	出版社只负责出版书籍，并通知到邮局
	"""
	def __init__(self):
		self.magazine = ["maga0"]
		self.newpaper = ["new0"]
		self.novel = ["nov0"]

	def publish_magazine(self, book_name):
		if book_name not in self.magazine:
			print("【出版社】出版新杂志了：%s" % (book_name))
			self.magazine.append(book_name)
			self.post_book("magazine", book_name)

	def publish_newpaper(self, book_name):
		if book_name not in self.newpaper:
			print("【出版社】卖报卖报啦: %s" % (book_name))
			self.newpaper.append(book_name)
			self.post_book("newpaper", book_name)

	def publish_novel(self, book_name):
		if book_name not in self.novel:
			print("【出版社】 出新书《%s》了..." % (book_name))
			self.novel.append(book_name)
			self.post_book("novel", book_name)


class Subscriber(object):
	"""
	读者只管在订阅后定期接收邮寄包裹
	"""
	def __init__(self, name, sex, years):
		self.name = name
		self.sex = sex
		self.years = years
		print("【读者】my name is %s,i'm %s years old..." % (self.name, self.years))

	def post(self, book_type, book_name):
		print("【读者】%s gets a new post: %s %s" % (self.name, book_type, book_name))


def main():
	po = Post_Office()
	ph = Publishing_House()
	s1 = Subscriber("张三", "man", 23)
	s2 = Subscriber("赵四", "woman", 30)
	s3 = Subscriber("王五", "man", 28)
	po.register("magazine", s1)
	po.register("novel", s2)
	po.register("newpaper", s3)
	ph.publish_magazine("青年文摘")
	ph.publish_newpaper("环球时报")
	ph.publish_novel("射雕英雄传")
	po.register("novel", s1)
	po.register("magazine", s2)
	ph.publish_newpaper("人民日报")
	ph.publish_novel("天龙八部")
	po.cancel("novel", s1)
	ph.publish_novel("倚天屠龙记")



	

if __name__ == "__main__":
	main()
