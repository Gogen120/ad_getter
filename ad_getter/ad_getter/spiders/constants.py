TAG_FIELD_MAP = {
    '*': '@value',
    '*': '@title',
    'span': 'text()',
    'a': 'text()',
    'button': 'text()',
    'div': 'text()'
}

SIMILAR_PRODUCT_TAGS = {
    'h2': 'text()',
    'u': 'text()',
    'div': 'text()',
    'header': 'text()',
    'span': 'text()'
}

DESCRIPTION_TAGS = {
    'span': 'text()',
    'a': 'text()',
    'div': 'text()',
    'h4': 'text',
    'i': 'text()',
    'li': 'text()',
    'p': 'text()',
    'label': 'text()',
    'h2': 'text()',
    'td': 'text()'
}

NOT_IN_SHOP_TAGS = {
    'strong': 'text()',
    'a': 'text()',
    'span': 'text()',
    'button': 'text()',
    'div': 'text()'
}

CHARS_TO_TRANSLATE = 'КВОСПДХНР'  # for case insensitive search

PRODUCT_KEYWORDS = ('купить', 'в корзину', 'оформить заказ', 'добавить в корзину', 'купить в 1 клик', 'купить в один клик', 'заказать', 'оформить заказ')
SIMILAR_PRODUCT_KEYWORDS = ('похожие товары', 'похожие продукты', 'похожие изделия', 'рекомендуем посмотреть', 'сопутствующие товары')
DESCRIPTION_KEYWORDS = ('описание', 'спецификация', 'характеристики', 'о товаре')
NOT_IN_SHOP_KEYWORDS = ('нет в наличии', 'под заказ', 'предзаказ', 'сообщить о поступлении')