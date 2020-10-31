
# 注
直接使用logging模块即可

# logie
simple logger for python

# examples
```python
import logie


logger = logie.Logger()
h1 = logie.StreamHandler(level='INFO')
logger.add_handler(h1)
h1 = logie.ColoredStreamHandler(level='debug')
logger.add_handler(h1)
f1 = logie.FileHandler(filename='logie.log')
logger.add_handler(f1)

logger.debug('debug msg')
logger.info('info msg %d', 3)
logger.warning('warning msg')
logger.error('error msg')
```

# TODOs
	future
```python
logging.basicConfig(
		level=logging.DEBUG,
	   	format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
	   	datefmt='%m-%d %H:%M',
	   	filename='/temp/myapp.log.%(created.year)s-%(created.month)s-%(created.day)s',
	   	filemode='w')

```
