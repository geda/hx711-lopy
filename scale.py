from hx711 import HX711
hx = HX711('G9', 'G10')
hx.set_scale(48.36)
hx.tare()
val = hx.get_units(5)
print(val)
