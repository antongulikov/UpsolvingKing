def main():

    import requests
    import json
    from users.models import Tag, TagProblem, Problem

    request_info = requests.get('http://codeforces.com/api/problemset.problems')
    if request_info.status_code != 200:
        main()
    text_request = request_info.text
    data = json.loads(text_request)
    if data['status'] != 'OK':
        return
    problems = data['result']['problems']
    statistic = data['result']['problemStatistics']

    print 'Get data from cf'

    diftags = set([])
    """ serch all digfferent tags"""
    for x in problems:
        for tag in x['tags']:
            diftags.add(tag)

    for name in diftags:

        tag = None

        try:
            tag = Tag.objects.get(name=name)
        except:
            tag = Tag.objects.create(name=name)

        if tag is None:
            main()

    print 'Updated all tags'

    for problem in problems:
        print problem['name']
        curent_problem = None
        try:
            curent_problem = Problem.objects.get(contest_id = problem['contestId'], problem_id = problem['index'])
        except:
            curent_problem = Problem.objects.create(contest_id = problem['contestId'], problem_id = problem['index'], problem_name = problem['name'])
        for tagname in problem['tags']:
            tag = Tag.objects.get(name=tagname)
            tag.problems.add(curent_problem)
            tag.save()

    for stat in statistic:
        print stat['contestId'],' ',stat['index']
        problem = Problem.objects.get(contest_id = stat['contestId'], problem_id = stat['index'])
        problem.solved = stat['solvedCount']
        problem.save()
        for tag in problem.tag_set.all():
            tp = None
            try:
                tp = TagProblem.objects.get(problem = problem, tag = tag)
                tp.cnt_solved = problem.solved
                tp.save()
            except:
                tp = TagProblem.objects.create(problem = problem, tag = tag, cnt_solved = problem.solved)