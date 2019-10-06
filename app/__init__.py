from flask import Flask,render_template,request,session
from flask import Flask, request, redirect, url_for

app = Flask(__name__ ,template_folder='../frontend/html',static_folder='../frontend')
posts ={
	"post1":{"article":[
		"Almost everyone, if given a chance would prefer the position a job giver instead of job seeker. Entrepreneurship gives u a chance to be a job giver. It’s a way to give it back to the society through the services you create. The precise definition of entrepreneurship is the process of creating new business or market. An entrepreneur usually starts a business form complete scratch , but one can also buy an old company n rebuild it. According to the job-listing site, Monster, there are nine characteristics of entrepreneurs and the entrepreneurial journey. They include motivation, creativity, hands-on, versatility, business skills, drive, vision, flexibility, and decisiveness.",
		"Generating an entrepreneurial mindset can improve how you think about business opportunities whether it’s for a small or large business, family-owned or venture-backed, or a social media entrepreneurship venture. Entrepreneurship training helps expose you to fundamental concepts and analytical tools such as the lean startup process to help improve your chance for success. Here at JNU we  work in hand in hand with you , matching shoulder to shoulder giving wings to your ideas and realization to your dreams.",
		"Not everyone knows that they want to be an entrepreneur. Many business creations happen because someone is trying to solve a need and they fall into entrepreneurship. New ventures seem to occur for entrepreneurs because they are trying to solve problems that exist in the world today. Self-employment is a critical reason why people choose to pursue their business ideas too. Here are some common qualities that good entrepreneurs have below that become success stories at a later time.",
		"Having a deep passion and or drive to complete something from start to finish is a common trait in many entrepreneurs. If you find yourself staying awake at night because you think you can fix something even better, or if you daydream on ways to improve something, you may be an entrepreneur without realizing it."
		],
		"heading":"Start Up",
		"img":"resources/img1.jpg"
		},
	"post2":{"article":[
		"Almost everyone, if given a chance would prefer the position a job giver instead of job seeker. Entrepreneurship gives u a chance to be a job giver. It’s a way to give it back to the society through the services you create. The precise definition of entrepreneurship is the process of creating new business or market. An entrepreneur usually starts a business form complete scratch , but one can also buy an old company n rebuild it. According to the job-listing site, Monster, there are nine characteristics of entrepreneurs and the entrepreneurial journey. They include motivation, creativity, hands-on, versatility, business skills, drive, vision, flexibility, and decisiveness.",
		"Generating an entrepreneurial mindset can improve how you think about business opportunities whether it’s for a small or large business, family-owned or venture-backed, or a social media entrepreneurship venture. Entrepreneurship training helps expose you to fundamental concepts and analytical tools such as the lean startup process to help improve your chance for success. Here at JNU we  work in hand in hand with you , matching shoulder to shoulder giving wings to your ideas and realization to your dreams.",
		"Not everyone knows that they want to be an entrepreneur. Many business creations happen because someone is trying to solve a need and they fall into entrepreneurship. New ventures seem to occur for entrepreneurs because they are trying to solve problems that exist in the world today. Self-employment is a critical reason why people choose to pursue their business ideas too. Here are some common qualities that good entrepreneurs have below that become success stories at a later time.",
		"Having a deep passion and or drive to complete something from start to finish is a common trait in many entrepreneurs. If you find yourself staying awake at night because you think you can fix something even better, or if you daydream on ways to improve something, you may be an entrepreneur without realizing it."
		],
	"heading":"E-Submit",
	"img":"resources/img2.jpg"},
	"post3":{"article":[
		"Almost everyone, if given a chance would prefer the position a job giver instead of job seeker. Entrepreneurship gives u a chance to be a job giver. It’s a way to give it back to the society through the services you create. The precise definition of entrepreneurship is the process of creating new business or market. An entrepreneur usually starts a business form complete scratch , but one can also buy an old company n rebuild it. According to the job-listing site, Monster, there are nine characteristics of entrepreneurs and the entrepreneurial journey. They include motivation, creativity, hands-on, versatility, business skills, drive, vision, flexibility, and decisiveness.",
		"Generating an entrepreneurial mindset can improve how you think about business opportunities whether it’s for a small or large business, family-owned or venture-backed, or a social media entrepreneurship venture. Entrepreneurship training helps expose you to fundamental concepts and analytical tools such as the lean startup process to help improve your chance for success. Here at JNU we  work in hand in hand with you , matching shoulder to shoulder giving wings to your ideas and realization to your dreams.",
		"Not everyone knows that they want to be an entrepreneur. Many business creations happen because someone is trying to solve a need and they fall into entrepreneurship. New ventures seem to occur for entrepreneurs because they are trying to solve problems that exist in the world today. Self-employment is a critical reason why people choose to pursue their business ideas too. Here are some common qualities that good entrepreneurs have below that become success stories at a later time.",
		"Having a deep passion and or drive to complete something from start to finish is a common trait in many entrepreneurs. If you find yourself staying awake at night because you think you can fix something even better, or if you daydream on ways to improve something, you may be an entrepreneur without realizing it."
		],
	"heading":"Cloud Computing",
	"img":"resources/img3.jpg"},
}
@app.route('/')
def home():
	print("Hello")
	return render_template("ecell.html")
@app.route('/sponser')
def sponser():
	return render_template("sponser.html")
@app.route('/article/<num>')
def article(num):
	if num.isnumeric():
		if(int(num)<=3):
			articles=posts["post"+num]
			return render_template("article.html",articles=articles)
	return render_template("ecell.html")
if __name__ == "__main__":
	app.run(debug=True)