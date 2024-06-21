import json

from database.models import User
from service.assistant.assistant import Assistant
from .data_for_create_assistants import data_assistant_value


class AssistantValue(Assistant):

    async def _create_assistant(self, model="gpt-4o", name="Mr Smith", **kwargs):
        assistant = await super()._create_assistant(model, name, **data_assistant_value, **kwargs)
        return assistant

    async def is_call_functions(self):
        if self._run.status == "requires_action":
            if self._run.required_action.submit_tool_outputs.tool_calls:
                return True
        return False

    async def is_valid_value(self, value: str) -> bool:
        content = f"""Is the following statement a traditional human value and free from misspellings or nonsense?
                    your answer can only be true or false.' Operator: {value}"""
        messages = [{"role": "user",
                     "content": content}]

        response = await self.client.chat.completions.create(model="gpt-4o", messages=messages, temperature=0.2,
                                                             max_tokens=1)
        response_message = response.choices[0].message.content
        print(response_message)

        return response_message.lower() == "true"

    async def pre_save_value(self) -> list:
        if not await self.is_call_functions():
            return []

        tool_outputs = []
        valid_values = []

        for tool in self._run.required_action.submit_tool_outputs.tool_calls:
            if tool.function.name == "save_value":
                user_value = json.loads(tool.function.arguments).get('value')
                is_valid = await self.is_valid_value(user_value)
                if is_valid:
                    valid_values.append(user_value)
                output = "Saved value successfully." if is_valid else "Couldn't save value."
                tool_outputs.append({"tool_call_id": tool.id, "output": output})

        if tool_outputs:
            try:
                self._run = await self.client.beta.threads.runs.submit_tool_outputs_and_poll(
                    thread_id=await self.get_thread_id(),
                    run_id=self._run.id,
                    tool_outputs=tool_outputs)

            except Exception as e:
                print("Failed to submit tool outputs:", e)

        return valid_values

    async def save_value(self, telegram_id) -> list:
        values = await self.pre_save_value()

        if values:
            user: User = await User.get(telegram_id=telegram_id)
            user = await user.add_values(values)
        return values
