from azure_content_safety.hosting import container
from azure_content_safety.protocols.i_content_safety import IContentSafety


async def main():
    content_safety = container[IContentSafety]

    result = await content_safety.text_moderation(
        text="I hate you",
        categories=["Hate", "Sexual", "SelfHarm", "Violence"],
    )
    print(result)


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
