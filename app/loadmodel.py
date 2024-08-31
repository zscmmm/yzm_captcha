from src.method.GTClick import GTClick
from src.method.GTnine import GTnine
from conf.config import gtconf

gt3word = GTClick(
    pdetect = gtconf['word']['pdetect'],
    per = gtconf['word']['per'], 
    pclass = gtconf['word']['pclass'], 
    pclasstags = gtconf['word']['pclasstags'], 
    chars_issorted = False,
    rmalpha = True,
)

gt3nine = GTnine(pclass=gtconf['nine']['pclass'])

gt4icon = GTClick(
    pdetect = gtconf['icon4mi']['pdetect'],
    per = gtconf['icon4mi']['per'], 
    pclass = gtconf['icon4mi']['pclass'], 
    pclasstags = gtconf['icon4mi']['pclasstags'], 
    chars_issorted = True,
    rmalpha = True,
)

