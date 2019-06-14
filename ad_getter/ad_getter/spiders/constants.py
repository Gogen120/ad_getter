BUY_TAGS = {
    'input': ('@value', '@title'),
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
    'td': 'text()',
    'h3': 'text()',
    'strong': 'text()'
}

NOT_IN_SHOP_TAGS = {
    'strong': 'text()',
    'a': 'text()',
    'span': 'text()',
    'button': 'text()',
    'div': 'text()',
    'td': 'text()'
}

REVIEW_TAGS = {
    'button': 'text()',
    'a': 'text()',
    'span': 'text()'
}

BUY_KEYWORDS = (
    'купить', 'в корзину', 'оформить заказ', 'добавить в корзину', 'купить в 1 клик',
    'купить в один клик', 'заказать', 'оформить заказ'
)
SIMILAR_PRODUCT_KEYWORDS = ('похожие товары', 'похожие продукты', 'похожие изделия', 'рекомендуем посмотреть')
DESCRIPTION_KEYWORDS = (
    'описание', 'спецификация', 'характеристики', 'о товаре', 'обзор',
    'все характеристики', 'преимущества'
)
NOT_IN_SHOP_KEYWORDS = (
    'нет в наличии', 'под заказ', 'предзаказ', 'сообщить о поступлении', 'ожидается поступление',
    'изделие отсутствует'
)
REVIEW_KEYWORDS = ('написать отзыв', 'добавить отзыв', 'оставить отзыв')

PRODUCT_ROUTES = '(collection|product|catalog|sankt-peterburg|shiny|diski|shop|store)'
EXTRA_ROUTES = '(/[\w\-%\=\.]+/?)+'
