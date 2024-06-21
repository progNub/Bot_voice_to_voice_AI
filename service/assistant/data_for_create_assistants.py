data_assistant_value = {
    'instructions': "Тебе необходимо выяснить у пользователя его ключевые ценности в формате диалога, 'вопрос-ответ'.",
    'tools':
        [{
            "type": "function",
            "function": {
                "name": "save_value",
                "description": "Сохранение ключевых ценностей юзера",
                "parameters": {"type": "object",
                               "properties": {
                                   "value": {"type": "string",
                                             "description": "Ценность юзера"},
                               },
                               "required": ["value"]
                               }
            }
        }]
}
