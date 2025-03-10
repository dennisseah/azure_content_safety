from azure_content_safety.hosting import container
from azure_content_safety.protocols.i_content_safety import IContentSafety


async def main():
    content_safety = container[IContentSafety]

    result = await content_safety.detect_protected_materials(
        text="Kiss me out of the bearded barley Nightly beside the green, green grass "
        "Swing, swing, swing the spinning step You wear those shoes and I will wear "
        "that dress Oh, kiss me beneath the milky twilight Lead me out on the moonlit "
        "floor Lift your open hand Strike up the band and make the fireflies dance "
        "Silver moon's sparkling So, kiss me Kiss me down by the broken tree house "
        "Swing me upon its hanging tire Bring, bring, bring your flowered hat We'll "
        "take the trail marked on your father's map."
    )
    print(result)


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
