import re, unicodedata



def remove_block_quotes(text):
    quotes = []
    modified_text = ''
    for line in text.split('\n'):
        if not line.strip().startswith('>'):
            modified_text += line + '\n'
        quotes.append(line)
    return modified_text, quotes



def remove_newlines(text):
    cleaned_text = re.sub(r"[\r\n]+", "", text)
    cleaned_text = re.sub(r"[\n\r]+", "", text)
    cleaned_text = re.sub(r"[\r]+", "", text)
    cleaned_text = re.sub(r"[\n]+", "", text)
    return cleaned_text



def remove_unicode(text): #With any combination and could be consecutive
    # Remove combining characters
    no_combining = unicodedata.normalize('NFKD', text)

    # Remove non-ASCII characters
    ascii_only = no_combining.encode('ascii', 'ignore').decode('ascii')

    # Remove remaining Unicode characters
    no_unicode = re.sub(r'[^\x00-\x7F]+', '', ascii_only)

    return no_unicode


def remove_extra_whitespaces(text):
    return ' '.join(text.split())


def remove_triple_quotes(text):
    occurrences = [m.start() for m in re.finditer('```', text)]
    idx = len(occurrences)
    if idx % 2 == 1:
        text = text[:occurrences[idx - 1]]
        idx = idx - 1
    for i in range(0, idx, 2):
        if idx > 0:
            text = text[:occurrences[idx - 2]] + text[(occurrences[idx - 1] + 3):]
            idx = idx - 2
    return text


def remove_stacktrace(text):
    st_regex = re.compile('at [a-zA-Z0-9\.<>$]+\(.+\)')
    lines = list()
    for line in text.split('\n'):
        matches = st_regex.findall(line.strip())
        if len(matches) == 0:
            lines.append(line)
        else:
            for match in matches:
                line = line.replace(match, ' ')
            lines.append(line.strip(' \t'))

    lines = '\n'.join(lines)
    # hack to get rid of multiple spaces in the text
    lines = ' '.join(lines.split())
    return lines

def remove_links(text):
    # Regular expression pattern to match links
    pattern = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'

    # Remove links from the text
    text_without_links = re.sub(pattern, '', text)
    
    return text_without_links
    


def filter_nontext(text):
    text = remove_links(text)
    text = remove_unicode(text)
    text = remove_block_quotes(text)[0]
    text = remove_stacktrace(text)
    text = remove_newlines(text)
    text = remove_triple_quotes(text)
    text = remove_extra_whitespaces(text)
    return text.strip()


def has_non_english_characters(text):
    try:
        text.encode(encoding='utf-8').decode('ascii')
    except UnicodeDecodeError:
        return True
    else:
        return False


def has_triple_quote_codes(text):
    if '```' in text:
        return True
    return False


def has_single_quote(text):
    # first remove triple quotes, then check single quotes
    text = remove_triple_quotes(text)
    if '`' in text:
        return True
    return False


def is_length_short(text):
    # checking the length after filtered
    if len(filter_nontext(text).split()) < 4:
        return True
    return False


def has_keyword_in_text(text):
    text = text.lower()
    keywords = ["head", "pull request", "master", "latest git", "pull req", "merged", " pr ", "latest",
                "commit", "fix"]
    for keyword in keywords:
        if keyword in text:
            return True
    return False


# "what do you think*", "can you verify*", "do/does * answer your question*
def filer_q_pattern(text):
    text = text.lower()
    match = re.search('what do you think*', text)
    if match is not None:
        return True
    match = re.search('can you verify*', text)
    if match is not None:
        return True
    match = re.search('(do/does) * answer your question*', text)
    if match is not None:
        return True
    return False


# if it returns true, filter the BR+question
def should_question_be_filtered(text):
    flag = has_non_english_characters(text)
    flag = flag | has_triple_quote_codes(text)
    flag = flag | has_single_quote(text)
    flag = flag | is_length_short(text)
    flag = flag | has_keyword_in_text(text)
    flag = flag | filer_q_pattern(text)
    return flag


# if it returns true, filter the BR
def should_title_be_filtered(text):
    flag = has_non_english_characters(text)
    return flag

# if it returns true, filter the BR
def should_post_be_filtered(text):
    flag = has_non_english_characters(text)
    return flag