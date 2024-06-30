import json

from database.models import User
from service.assistant.assistant import Assistant
from .data_for_create_assistants import CreateAssistantData, CheckValueFunction


class AssistantValue(Assistant):

    async def _create_assistant(self, model="gpt-4o", name="Mr Smith", **kwargs):
        assistant = await super()._create_assistant(model, name, **CreateAssistantData.get_params(), **kwargs)
        return assistant

    async def is_call_functions(self):
        if self._run.status == "requires_action":
            if self._run.required_action.submit_tool_outputs.tool_calls:
                return True
        return False

    async def is_valid_value(self, value: str) -> bool:
        messages = [{"role": "user", "content": value}]
        functions = [CheckValueFunction.get_function()]
        tool_choice = {"type": "function", "function": {"name": CheckValueFunction.name}}
        try:
            response = await self.client.chat.completions.create(model="gpt-4o", messages=messages, tools=functions,
                                                                 tool_choice=tool_choice)
            for tool in response.choices[0].message.tool_calls:
                if tool.function.name == CheckValueFunction.name:
                    is_human_value: str = json.loads(tool.function.arguments).get('is_human_value')
                    return is_human_value.lower() == "true"
        except Exception as e:
            print("Failed to check value:", e)

    async def pre_save_value(self) -> list:
        if not await self.is_call_functions():
            return []

        tool_outputs = []
        valid_values = []

        for tool in self._run.required_action.submit_tool_outputs.tool_calls:
            if tool.function.name == CreateAssistantData.name_function:
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
            user: User = await User.get_object_or_none(telegram_id=telegram_id)
            await user.add_values(values)
        return values
