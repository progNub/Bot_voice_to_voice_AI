import base64
import uuid
from pathlib import Path
from typing import BinaryIO

import aiofiles
from aiogram.types import PhotoSize

from loader import client_openai as client, bot


class VisionManager:

    def __init__(self, photo: list[PhotoSize], _path_to_save=Path('data/images/')):
        self.photo = photo[-1]
        self._filename: str = ''
        self._path_to_save = _path_to_save

    async def get_file(self) -> BinaryIO:
        file_image = await bot.get_file(self.photo.file_id)
        file = await bot.download_file(file_image.file_path)
        return file

    async def get_filename(self) -> Path:
        file_image = await bot.get_file(self.photo.file_id)
        if not self._filename:
            filename = str(uuid.uuid4()) + file_image.file_path.split('/')[-1]
            self._filename = Path(filename)
        return self._filename

    async def get_file_path(self) -> Path:
        file_path = self._path_to_save / (await self.get_filename())
        return file_path

    async def save_file(self):
        if not self._path_to_save.exists():
            self._path_to_save.mkdir(parents=True, exist_ok=True)

        async with aiofiles.open(await self.get_file_path(), 'wb') as file:
            await file.write((await self.get_file()).read())

    async def get_encoded_file(self):
        await self.save_file()
        async with aiofiles.open(await self.get_file_path(), "rb") as image_file:
            content = await image_file.read()
            return base64.b64encode(content).decode('utf-8')

    async def delete_file(self):
        file = await self.get_file_path()
        file.unlink()
        return f'File {file} has been deleted'


class Vision(VisionManager):

    def __init__(self, photo: list[PhotoSize]):
        super().__init__(photo=photo)

    async def analise_emotions(self) -> str:
        base64_image = await self.get_encoded_file()
        await self.delete_file()
        """Analyze the emotions of a person in a photo"""
        try:
            response = await client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": "What is the mood of the person in the photo?"},
                            {"type": "image_url", "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}"
                            }
                             }, ], }],
                max_tokens=300, )
        except Exception as e:
            print(f'Error in analyze_emotions: {e}')
            return f'Error in analyze_emotions: {e}'

        answer_message = response.choices[0].message.content

        return answer_message
