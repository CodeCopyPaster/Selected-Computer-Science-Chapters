import input_checker

def process_text(text):
    # Split text by words
    words = text.split()

    # a) count words with len < 6
    short_words_count = sum(1 for word in words if len(word) < 6)
    print(f"Count of words with len < 6: {short_words_count}")

    # b) find the shortest word with "w" in the end
    words_ending_with_w = [word for word in words if word.endswith('w')]
    if words_ending_with_w:
        shortest_word = min(words_ending_with_w, key=len)
        print(f"The shortest word with 'w' in the end: {shortest_word}")
    else:
        print("There are no word with 'w' in the end.")

    # c) print sorted words by length
    sorted_words = sorted(words, key=len)
    print("Sorted words by their length:")
    for word in sorted_words:
        print(word)


def task4():
    """
        This function count words with length lower than 6,
        find the shortest word with last letter = w,
        sort words by their length
    :return: words which len < 6, shortest word with "w" in the end, sorted words by length
    """

    # Input choose
    choice = input_checker.input_checker("Input:"
                                         "\n1 -> for finished text"
                                         "\n2 -> for random input", int, 1, 2)


    text = "So she was considering in her own mind, as well as she could, for the hot day made her feel very sleepy and stupid, whether the pleasure of making a daisy-chain would be worth the trouble of getting up and picking the daisies, when suddenly a White Rabbit with pink eyes ran close by her."

    random_generated_text = input_checker.random_input(str,10,50)

    if choice == 1:
        process_text(text)
    else:
        process_text(random_generated_text)


