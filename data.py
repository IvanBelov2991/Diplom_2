import random

bun_ingredient = '61c0c5a71d1f82001bdaaa6c'
sauce_ingredient = '61c0c5a71d1f82001bdaaa75'
filling_ingredient = '61c0c5a71d1f82001bdaaa70'
order_body = {"ingredients": [bun_ingredient, sauce_ingredient, filling_ingredient]}
order_body_with_sauce_ingredient = {"ingredients": [sauce_ingredient]}
order_body_with_filling_ingredient = {"ingredients": [filling_ingredient]}
fake_ingredient = {"ingredients": ''.join([str(random.randint(0, 9)) for _ in range(24)])}
