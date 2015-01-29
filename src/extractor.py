from bs4 import BeautifulSoup, NavigableString


def extract_text_internal(root, text, level, max_level):
    if level > max_level:
        return ''

    if type(root) is NavigableString:
        return text + root

    children_text = ''
    for child in root.children:
        children_text += extract_text_internal(child,
                                               text, level + 1, max_level)

    return children_text


def extract_text(root):
    return extract_text_internal(root, '', 0, 1)


class Extractor(object):

    def __init__(self, tree):
        self.tree = tree

    def extract(self):
        candidate_paras = self.gather_first_children_with_tag('p')
        possible_review_texts = [' '.join(self.compute_tag_word_context(p))
                                 for p in candidate_paras]
        return max(possible_review_texts, key=lambda t: len(t))

    def gather_first_children_with_tag(self, tag):
        tagged_elements = self.tree.find_all(tag)
        return [el for el in tagged_elements if el.previous_sibling is None
                or type(el.previous_sibling) is NavigableString]

    def compute_tag_word_context(self, tag):
        review_text = [extract_text(tag)]

        all_siblings = tag.next_siblings
        for sibling in all_siblings:
            review_text.append(extract_text(sibling))

        return review_text


test_document = f = open('../test/fixture.html', 'r')

e = Extractor(BeautifulSoup(test_document))
print e.extract()
