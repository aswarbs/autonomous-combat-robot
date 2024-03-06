import qrcode

img = qrcode.make('top_left_facing_south')
img.save("top_left_facing_south.png")
img = qrcode.make('top_left_facing_east')
img.save("top_left_facing_east.png")

img = qrcode.make('top_right_facing_south')
img.save("top_right_facing_south.png")
img = qrcode.make('top_right_facing_west')
img.save("top_right_facing_west.png")

img = qrcode.make('bottom_left_facing_north')
img.save("bottom_left_facing_north.png")
img = qrcode.make('bottom_left_facing_east')
img.save("bottom_left_facing_east.png")

img = qrcode.make('bottom_right_facing_north')
img.save("bottom_right_facing_north.png")
img = qrcode.make('bottom_right_facing_west')
img.save("bottom_right_facing_west.png")