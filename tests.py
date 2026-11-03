import pytest
from model import Question

@pytest.fixture
def question_with_choices():
    question = Question(title='Capital of Brazil?', max_selections=2)
    question.add_choice('Brasilia', True)
    question.add_choice('Rio de Janeiro', False)
    question.add_choice('Sao Paulo', False)
    return question


def test_fixture_question_contains_multiple_choices(question_with_choices):
    assert len(question_with_choices.choices) == 3
    assert question_with_choices.choices[0].text == 'Brasilia'
    assert question_with_choices.choices[0].is_correct


def test_fixture_question_corrects_selected_choices(question_with_choices):
    correct_choice = question_with_choices.choices[0]
    incorrect_choice = question_with_choices.choices[1]

    result = question_with_choices.correct_selected_choices(
        [correct_choice.id, incorrect_choice.id]
    )

    assert result == [correct_choice.id]


def test_create_question():
    question = Question(title='q1')
    assert question.id != None

def test_create_multiple_questions():
    question1 = Question(title='q1')
    question2 = Question(title='q2')
    assert question1.id != question2.id

def test_create_question_with_invalid_title():
    with pytest.raises(Exception):
        Question(title='')
    with pytest.raises(Exception):
        Question(title='a'*201)
    with pytest.raises(Exception):
        Question(title='a'*500)

def test_create_question_with_valid_points():
    question = Question(title='q1', points=1)
    assert question.points == 1
    question = Question(title='q1', points=100)
    assert question.points == 100

def test_create_choice():
    question = Question(title='q1')
    
    question.add_choice('a', False)

    choice = question.choices[0]
    assert len(question.choices) == 1
    assert choice.text == 'a'
    assert not choice.is_correct

def test_question_uses_default_values():
    question = Question(title='Question')

    assert question.points == 1
    assert question.max_selections == 1
    assert question.choices == []


def test_create_question_with_invalid_points():
    with pytest.raises(Exception):
        Question(title='Question', points=0)

    with pytest.raises(Exception):
        Question(title='Question', points=101)


def test_add_choice_returns_created_choice():
    question = Question(title='Question')

    choice = question.add_choice('Alternative A', True)

    assert choice is question.choices[0]
    assert choice.text == 'Alternative A'
    assert choice.is_correct


def test_choices_receive_sequential_ids():
    question = Question(title='Question')

    first_choice = question.add_choice('Alternative A')
    second_choice = question.add_choice('Alternative B')

    assert first_choice.id == 1
    assert second_choice.id == 2


def test_choice_text_cannot_be_empty():
    question = Question(title='Question')

    with pytest.raises(Exception):
        question.add_choice('')


def test_choice_text_cannot_exceed_100_characters():
    question = Question(title='Question')

    with pytest.raises(Exception):
        question.add_choice('a' * 101)


def test_remove_choice_by_id():
    question = Question(title='Question')
    first_choice = question.add_choice('Alternative A')
    second_choice = question.add_choice('Alternative B')

    question.remove_choice_by_id(first_choice.id)

    assert question.choices == [second_choice]


def test_remove_all_choices():
    question = Question(title='Question')
    question.add_choice('Alternative A')
    question.add_choice('Alternative B')

    question.remove_all_choices()

    assert question.choices == []


def test_set_correct_choices():
    question = Question(title='Question', max_selections=2)
    first_choice = question.add_choice('Alternative A')
    second_choice = question.add_choice('Alternative B')

    question.set_correct_choices([first_choice.id, second_choice.id])

    assert first_choice.is_correct
    assert second_choice.is_correct


def test_correct_selected_choices_returns_only_correct_answers():
    question = Question(title='Question', max_selections=2)
    correct_choice = question.add_choice('Alternative A', True)
    incorrect_choice = question.add_choice('Alternative B', False)

    result = question.correct_selected_choices(
        [correct_choice.id, incorrect_choice.id]
    )

    assert result == [correct_choice.id]