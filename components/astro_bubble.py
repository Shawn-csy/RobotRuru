from linebot.models import (
    FlexSendMessage,
    BubbleContainer,
    BoxComponent,
    TextComponent
)

def create_fortune_box(title, star_count, content, icon):
    """生成單個運勢區塊"""
    return BoxComponent(
        layout='vertical',
        backgroundColor='#F4F1EA',
        cornerRadius='md',
        paddingAll='sm',
        borderWidth='1px',
        borderColor='#D3D0CB',
        contents=[
            BoxComponent(
                layout='horizontal',
                contents=[
                    TextComponent(
                        text=f"{icon} {title}",
                        weight='bold',
                        color='#4A5759',
                        size='sm',
                        flex=3
                    ),
                    TextComponent(
                        text="★"*star_count + "☆"*(5-star_count),
                        size='xs',
                        color='#9C7C38',
                        flex=2,
                        align='end'
                    )
                ]
            ),
            TextComponent(
                text=content,
                size='xs',
                wrap=True,
                margin='sm',
                color='#4A5759'
            )
        ]
    )

def create_astro_bubble(title, star_counts, reminder, starreminder=None):
    fortune_icons = ["🎯", "💝", "💼", "💰"]
    fortune_titles = ["整體運勢", "愛情運勢", "事業運勢", "財運運勢"]
    
    fortune_boxes = [
        create_fortune_box(title, count, content, icon)
        for (count, content), title, icon 
        in zip(star_counts, fortune_titles, fortune_icons)
    ]
    footer_contents = []
    # 如果有速配星座，添加速配星座區塊
    if starreminder:
        footer_contents.extend([
            TextComponent(
                text="💫 速配星座",
                weight='bold',
                color='#4A5759',
                size='xs',
                align='center'
            ),
            TextComponent(
                text=starreminder,
                color='#4A5759',
                size='xs',
                wrap=True,
                align='center',
                margin='sm'
            )
        ])

    # 添加提醒區塊
    footer_contents.extend([
        TextComponent(
            text="💫 " + ("每週提醒" if starreminder else "今日小叮嚀"),
            weight='bold',
            color='#4A5759',
            size='xs',
            align='center',
            margin='md' if starreminder else None
        ),
        TextComponent(
            text=reminder,
            color='#4A5759',
            size='xs',
            wrap=True,
            align='center',
            margin='sm'
        )
    ])

    return BubbleContainer(
        size='kilo',
        header=BoxComponent(
            layout='vertical',
            backgroundColor='#4A5759',
            paddingAll='md',
            contents=[
                TextComponent(
                    text=title,
                    weight='bold',
                    size='lg',
                    color='#4A5759',
                    align='center'
                )
            ]
        ),
        body=BoxComponent(
            layout='vertical',
            backgroundColor='#EDEAE5',
            paddingAll='md',
            spacing='sm',
            contents=fortune_boxes
        ),
        footer=BoxComponent(
            layout='vertical',
            backgroundColor='#4A5759',
            paddingAll='md',
            contents=footer_contents
        )
    )

