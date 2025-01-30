from scores import Scores

def sort_scores_test(scores):
    scores_copy = scores.copy()
    scores_copy = list(reversed(sorted(scores_copy, key=lambda tuple: tuple[1])))
    for i in range(len(scores)):
        name, score1 = Scores().sort_scores(scores)[i]
        name, score2 = scores_copy[i]
        assert score1 == score2

def test_get_scores():
    with open('get_scores.txt', 'w') as f:
        f.write("1 test 100")
        f.write("2 test 200")
        f.write("3 test 150")

    expected_scores = [('test', 100), ('test', 200), ('test', 150)]

    scores = Scores().get_scores()

    assert scores == expected_scores