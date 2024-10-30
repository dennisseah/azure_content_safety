import base64
import os

from azure_content_safety.hosting import container
from azure_content_safety.protocols.i_content_safety import IContentSafety


async def main():
    content_safety = container[IContentSafety]

    with open(os.path.join("samples", "test_image.jpg"), "rb") as f:
        image_str = base64.b64encode(f.read()).decode("utf-8")

    result = await content_safety.image_moderation(image=image_str)
    print(result)


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
