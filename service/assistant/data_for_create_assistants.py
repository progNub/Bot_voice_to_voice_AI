class CreateAssistantData:
    name_function = "save_value"

    @classmethod
    def get_params(cls):
        return {
            'instructions':
                "You need to find out the user's key values in a question-and-answer dialogue format.",
            'tools':
                [{"type": "function",
                  "function": {"name": F"{cls.name_function}",
                               "description": "Saving the user's key values",
                               "parameters": {"type": "object",
                                              "properties": {
                                                  "value": {"type": "string",
                                                            "name": "User's value"}},
                                              "required": ["value"]}}}]}


class CheckValueFunction:
    name = "check_human_value"

    @classmethod
    def get_function(cls):
        return {"type": "function",
                "function": {
                    "name": f"{cls.name}",
                    "description": "Check if the text represents a traditional human value",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "is_human_value": {
                                "type": "string",
                                "name": "Answer to the question of whether this is a value",
                                "enum": ["False", "True"]}},
                        "required": ["is_human_value"], }}}
