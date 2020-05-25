import sys
import vk_api


def load_posts(login, password):
    vk_session = vk_api.VkApi(login, password)

    try:
        vk_session.auth(token_only=True)
    except vk_api.AuthError as error_msg:
        print(error_msg)

    vk = vk_session.get_api()

    groups = vk.groups.search(q='Подслушано', sort=2, count=10)
    group_names = [item['screen_name'] for item in groups['items'] if '18+' not in item['name']]

    group_posts = {}
    for i, name in enumerate(group_names):
        if i % 10 == 0:
            print(f'getting wall of "{name}", group {i} of {len(group_names)}', file=sys.stderr)
        wall = vk.wall.get(domain=name, count=100)
        group_posts[name] = [item['text'] for item in wall['items']]

    return group_posts

