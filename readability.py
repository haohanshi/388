from textstat.textstat import textstat

test_data = """Playing games has always been thought to be important to the development of well-balanced and creative children; however, what part, if any, they should play in the lives of adults has never been researched that deeply. I believe that playing games is every bit as important for adults as for children. Not only is taking time out to play games with our children and other adults valuable to building interpersonal relationships but is also a wonderful way to release built up tension."""

# * 90-100 : Very Easy 
# * 80-89 : Easy 
# * 70-79 : Fairly Easy 
# * 60-69 : Standard 
# * 50-59 : Fairly Difficult 
# * 30-49 : Difficult 
# * 0-29 : Very Confusing
print textstat.flesch_reading_ease(test_data)

print textstat.smog_index(test_data)
# The result is a number that corresponds with a U.S. grade level.
print textstat.flesch_kincaid_grade(test_data)
# its output approximates the U.S. grade level thought necessary to comprehend the tex    
print textstat.coleman_liau_index(test_data)
# if the ARI is 6.5, then the grade level to comprehend the text is 6th to 7th grade.
print textstat.automated_readability_index(test_data)
# 4.9 or lower    easily understood by an average 4th-grade student or lower
# 5.0–5.9    easily understood by an average 5th or 6th-grade student
# 6.0–6.9    easily understood by an average 7th or 8th-grade student
# 7.0–7.9    easily understood by an average 9th or 10th-grade student
# 8.0–8.9    easily understood by an average 11th or 12th-grade student
# 9.0–9.9    easily understood by an average 13th to 15th-grade (college) student
# 10.0 or higher    easily understood by an average college graduate
print textstat.dale_chall_readability_score(test_data)

print textstat.difficult_words(test_data)
# If your answer is 10, you have written at the 10th grade in high school. If your answer is 14, then it would take a sophomore in college to understand your writing.
print textstat.linsear_write_formula(test_data)
# The Gunning Fog Index gives the number of years of education that your reader hypothetically needs to understand the paragraph or text
print textstat.gunning_fog(test_data)
# Based upon all the above tests returns the best grade level under which the given text belongs to.
print textstat.text_standard(test_data)