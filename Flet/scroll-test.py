from flet import *

def main(page:Page):
	page.scroll = "always"


	# NOW I CUSTMIZE STYLE SCROLLBAR
	page.theme = Theme(
	scrollbar_theme = ScrollbarTheme(
		# NOW I CHANGE TRACK COLOR FROM SCROLLBAR
		track_color={
			MaterialState.HOVERED:"green",
			# AND FOR DEFAULT AND NO HOVER 
			# I SET TO TRANSPARENT
			MaterialState.DEFAULT:colors.TRANSPARENT,

			},
		track_visibility=True,
		# AND I SET BORDER COLOR SCROLLBAR
		track_border_color="blue",
		thumb_visibility=True,
		# now I CHANGE SCROLLBAR COLOR 
		thumb_color={
			MaterialState.HOVERED:"purple",
			# AND FOR DEFAULT AND NO HOVER 
			# I SET TO TRANSPARENT
			MaterialState.DEFAULT:"grey",

			},
		# NOW I CHANGE WEIGHT OF SCROLLBAR
		thickness=30,
		# AND ADD RADIUS BORDER
		radius=20,

		# AND YOU CAN SET SCROLLBAR TOP MARGIN
		# YOU SEE SPACE IN TOP SCROLLBAR
		main_axis_margin=40,

		# AND YOU CAN SET MARGIN OF SCROLLBAR LIKE THIS
		# YOU SEE SPACE IN LEFT AND RIGHT FROM SCROLLBAR
		# THAT YOU SET THIS

		cross_axis_margin=50,



		)
		)

	bd = Column(
		# ENABLE SCROLL 
		# scroll="always"
		)

	# NOW I ADD DATA to bd with loop 
	for x in range(0,30):
		bd.controls.append(
			# I SEND TEXT HERE
		Text(f"fake data {x}",size=20)

			)


	page.add(bd)

app(target=main)