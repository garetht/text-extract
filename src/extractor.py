from bs4 import BeautifulSoup, NavigableString, Comment


def extract_text_internal(root, text, level, max_level):
    if level > max_level:
        return ''

    if type(root) is NavigableString:
        return text + root

    if type(root) is Comment:
        return text

    if root.name is "script":
        return text

    children_text = ''
    for child in root.children:
        children_text += extract_text_internal(child,
                                               text, level + 1, max_level)

    return children_text


def extract_text(root):
    return extract_text_internal(root, '', 0, 2)


class Extractor(object):
    """
    This works quite simply but effectively.
    1. We find all paragraph tags that are first
    children.
    2. We iterate through the tag's siblings and extract
    text down to a maximum of two levels.
    3. We return the text from the paragraph tag that
    is the longest.
    """

    def extract(self, tree):
        self.tree = tree
        candidate_paras = self.gather_first_children_with_tag('p')
        possible_review_texts = [' '.join(self.compute_tag_word_context(p))
                                 for p in candidate_paras]
        if len(possible_review_texts) > 0:
            return max(possible_review_texts, key=lambda t: len(t))
        else:
            return ''

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
