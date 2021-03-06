import re,json

class Course:
	def grade_to_min_json(self):
    		"""
			Course: Indexes by Course NameError
			Quarter: Indexes by quarter
			Else: Just returns JSON blob
		"""
		temp_dict = {}
		temp_dict["course"] = "%s %s" % (self.department, self.course)
		temp_dict["quarter"] = "%s%s" % (self.quarter, self.year)
		temp_dict["grade"] = self.grade
		temp_dict["units"] = self.units
		return temp_dict["course"],temp_dict["quarter"], json.dumps(temp_dict)

	def __init__(self, quarter, year, department, course, units, grade):
		self.quarter = quarter
		self.year = year
		self.department = department
		self.course = course
		self.units = units
		self.grade = grade

	def grade_to_full_json(self):
		temp_dict = {}
		temp_dict["quarter"] = self.quarter + self.year
		temp_dict["department"] = self.department
		temp_dict["course"] = self.course
		temp_dict["units"] = self.units
		temp_dict["grade"] = self.grade
		return json.dumps(temp_dict)



def get_grade_arr(html_doc):
	disallowed = ("TP","NR", "WIP")
	grades = re.findall("[A-Z]+[0-9]{1,3}[ ]+[A-Z]*[ ]*[A-Z]+[ ]*[0-9]*[A-Z]*[ ]+[0-9].[0-9][ ]+[A-Z]+[+,-]?", html_doc)
	grade_arr = []
	for grade in grades:
		grade = grade.split() #splits string by white spaces
		grade[:] = [x for x in grade if x != " "] #remove all white space elements
		if not grade[1].isalpha(): #checks for cases where department + course number are concantenated
			new_grade = re.findall(r"[^\W\d_]+|\d+", grade[1]) #splits the string between alpha and numeric
			grade[1] = new_grade[0]
			grade.insert(2, new_grade[1])
		if len(grade[1]) > 4:
			continue
		temp_year = grade[0]
		grade[0] = temp_year[:2]
		grade.insert(1, temp_year[2:])
		grade = Course(grade[0], grade[1], grade[2], grade[3], grade[4], grade[5])
		if grade.grade not in disallowed:
			grade_arr.append(grade)
	return grade_arr



