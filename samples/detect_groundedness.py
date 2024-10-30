from azure_content_safety.hosting import container
from azure_content_safety.protocols.i_content_safety import IContentSafety, QnAQuery


async def main():
    content_safety = container[IContentSafety]

    result = await content_safety.detect_groundedness(
        domain="Generic",
        task="QnA",
        qna=QnAQuery(
            query="How much does she currently get paid per hour at the bank?"
        ),
        text="12/hour",
        groundingSources=[
            "I'm 21 years old and I need to make a decision about the next two years "
            "of my life. Within a week. I currently work for a bank that requires "
            "strict sales goals to meet. IF they aren't met three times (three months) "
            "you're canned. They pay me 10/hour and it's not unheard of to get a raise "
            "in 6ish months. The issue is, **I'm not a salesperson**. That's not my "
            "personality. I'm amazing at customer service, I have the most positive "
            'customer service "reports" done about me in the short time I\'ve worked '
            'here. A coworker asked "do you ask for people to fill these out? you '
            'have a ton". That being said, I have a job opportunity at Chase Bank as '
            "a part time teller. What makes this decision so hard is that at my "
            "current job, I get 40 hours and Chase could only offer me 20 hours/week. "
            "Drive time to my current job is also 21 miles **one way** while Chase "
            "is literally 1.8 miles from my house, allowing me to go home for lunch. "
            "I do have an apartment and an awesome roommate that I know wont be late "
            "on his portion of rent, so paying bills with 20hours a week isn't the "
            "issue. It's the spending money and being broke all the time.\n\nI "
            "previously worked at Wal-Mart and took home just about 400 dollars every "
            "other week. So I know i can survive on this income. I just don't know "
            "whether I should go for Chase as I could definitely see myself having a "
            "career there. I'm a math major likely going to become an actuary, so "
            "Chase could provide excellent opportunities for me **eventually**."
        ],  # noqa E501
        reasoning=False,
    )
    print(result)


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
