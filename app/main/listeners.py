def notify_item_created(item):
    # Could send an email, webhook, push notification, etc.
    print(f"[Listener] Communication item created: {item.content}")
