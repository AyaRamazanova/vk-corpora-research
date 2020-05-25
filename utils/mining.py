import sys
import vk_api
from nltk import sent_tokenize, wordpunct_tokenize, download
from pymorphy2 import MorphAnalyzer

download('punkt')
download('wordnet')
download('averaged_perceptron_tagger')


def load_posts(login, password):
    vk_session = vk_api.VkApi(login, password)

    try:
        vk_session.auth(token_only=True)
    except vk_api.AuthError as error_msg:
        print(error_msg)

    vk = vk_session.get_api()

    # Searching groups by pattern
    group_search = vk.groups.search(q='Подслушано', sort=2, count=100)

    group_screen_names = [
        group['screen_name'] for group in group_search['items']
        if '18+' not in group['name']
    ]
    group_screen_names.append('ortoblogge')
    group_screen_names.append('indulgencia')

    # Getting additional metainfo
    groups_info = vk.groups.getById(group_ids=group_screen_names,
                                    fields=['description', 'members_count'])

    # Filtering results
    group_data = {}
    for group in groups_info:
        if group['is_closed'] == 0:
            group_data[group['screen_name']] = {
                'name': group['name'],
                'description': group['description'],
                'members_count': group['members_count']
            }

    # Adding groups texts
    for i, screen_name in enumerate(group_data):
        print(
            f'getting wall of "{screen_name}", group {i} of {len(group_data)}',
            file=sys.stderr)
        wall = vk.wall.get(domain=screen_name, count=100)
        group_data[screen_name]['texts'] = [
            item['text'] for item in wall['items']
        ]

    return group_data


def to_corpora(group_data):
    m = MorphAnalyzer()
    for gr_num, name in enumerate(group_data):
        print(f'processing "{name}", group {gr_num} of {len(group_data)}',
              file=sys.stderr)
        posts = group_data[name]['texts']
        for i, post in enumerate(posts):
            post = post.split('\n\n')
            for j, paragraph in enumerate(post):
                paragraph = sent_tokenize(paragraph)
                for k, sentence in enumerate(paragraph):
                    sentence = wordpunct_tokenize(sentence)
                    for l, word in enumerate(sentence):
                        p = m.parse(word)[0]
                        word = {p.normal_form: p.tag.POS}
                        sentence[l] = word
                    paragraph[k] = sentence
                post[j] = paragraph
            posts[i] = post
        group_data[name]['texts'] = posts
    return group_data
