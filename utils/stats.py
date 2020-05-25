import pandas as pd


def words_per_post(posts):
    words_num = 0.
    for post in posts:
        for paragraph in post:
            for sentence in paragraph:
                words_num += len(sentence)
    mean_word_num = words_num / len(posts)
    return mean_word_num


def words_per_sentence(posts):
    words_num = 0.
    sent_num = 0.
    for post in posts:
        for paragraph in post:
            sent_num += len(paragraph)
            for sentence in paragraph:
                words_num += len(sentence)
    mean_words = words_num / sent_num
    return mean_words


def pos_per_post(posts, pos):
    """To count number of occurrences of a particular part of speech in posts"""
    pos_num = 0.
    for post in (posts):
        for paragraph in post:
            for sentence in paragraph:
                for words in sentence:
                    for name in words.keys():
                        if words[name] == pos:
                            pos_num += 1
    return pos_num / len(posts)


def group_dict(posts, pos=None):
    gr_dict = {}
    for post in posts:
        for paragraph in post:
            for sentence in paragraph:
                for word in sentence:
                    for name in word.keys():
                        if pos is None or pos == word[name]:
                            gr_dict[name] = gr_dict.setdefault(name, 0) + 1
    return gr_dict


def top_words(posts, num=10, pos=None):
    gr_dict = group_dict(posts, pos)
    sorted_dict = list(gr_dict.items())
    sorted_dict.sort(key=lambda i: i[1], reverse=True)
    num = min(len(gr_dict), num)
    return [x[0] for x in sorted_dict[:num]]


def to_stat_frame(group_data):
    corpora_frame = pd.DataFrame()
    corpora_frame['group'] = [
        group_data[group]['name'] for group in group_data
    ]
    corpora_frame['memb_count'] = [
        group_data[group]['members_count'] for group in group_data
    ]
    corpora_frame['description'] = [
        group_data[group]['description'] for group in group_data
    ]

    corpora_frame['words_per_post'] = [
        words_per_post(group_data[group]['texts']) for group in group_data
    ]
    corpora_frame['words_per_sentence'] = [
        words_per_sentence(group_data[group]['texts']) for group in group_data
    ]

    corpora_frame['noun_num'] = [
        pos_per_post(group_data[group]['texts'], 'NOUN')
        for group in group_data
    ]
    corpora_frame['top_noun'] = [
        top_words(group_data[group]['texts'], pos='NOUN')
        for group in group_data
    ]

    corpora_frame['adjf_num'] = [
        pos_per_post(group_data[group]['texts'], 'ADJF')
        for group in group_data
    ]
    # corpora_frame['top_adjf'] = [top_words(data[group]['texts'], pos = 'ADJF') for group in group_names]

    corpora_frame['verb_num'] = [
        pos_per_post(group_data[group]['texts'], 'VERB')
        for group in group_data
    ]
    # corpora_frame['top_verb'] = [top_words(data[group]['texts'], pos = 'VERB') for group in group_names]
    return corpora_frame
