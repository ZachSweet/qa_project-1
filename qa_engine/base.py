
import pandas as pd
from nltk.parse import DependencyGraph
from nltk.tree import Tree
from collections import defaultdict

DATA_DIR = "data/"
QUESTION_FILE = "hw6-questions.csv"
ANSWER_FILE = "hw6-answers.csv"
STORIES_FILE = "hw6-stories.csv"

RESPONSE_FILE = "hw6-responses.csv"

import math

from collections import defaultdict


def prepare_deps(raw_deps):

    if type(raw_deps) == float and math.isnan(raw_deps):
        return []
    return [DependencyGraph(dep, top_relation_label="root") for dep in raw_deps.split("\n\n")
            if len(dep) > 2]


def prepare_pars(raw_pars):
    if type(raw_pars) == float and math.isnan(raw_pars):
        return []

    return [Tree.fromstring("(ROOT "+line.strip().rstrip(" \n\t"))
            for line in raw_pars.split("\n") if len(line) > 2]


def prepare_story_data(df):
    stories = {}
    for row in df.itertuples():
        this_story = {
            "story_dep": prepare_deps(row.story_dep),
            "sch_dep": prepare_deps(row.sch_dep),
            "sch_par": prepare_pars(row.sch_par),
            "story_par": prepare_pars(row.sch_par),
            "sch": row.sch,
            "text": row.text,
            "sid": row.sid,
        }
        stories[row.sid] = this_story
    return stories


def prepare_questions(df):
    questions = {}
    for row in df.itertuples():
        this_qstn = {
            "dep": prepare_deps(row.dep)[0],
            "par": prepare_pars(row.par)[0],
            "text": row.text,
            "sid": row.sid,
            "difficulty": row.difficulty,
            "type": row.type,
            "qid": row.qid
        }
        questions[row.qid] = this_qstn
    return questions


class QABase(object):

    def __init__(self):

        self._stories = prepare_story_data(pd.read_csv(DATA_DIR + STORIES_FILE))
        self._questions = prepare_questions(pd.read_csv(DATA_DIR + QUESTION_FILE))
        self._answers = {q["qid"]: "" for q in self._questions.values()}


    @staticmethod
    def answer_question(question, story):
        raise NotImplemented


    def get_question(self, qid):
        return self._questions.get(qid)


    def get_story(self, sid):
        return self._stories.get(sid)


    def run(self):
        for qid, q in self._questions.items():
            a = self.answer_question(q, self._stories.get(q["sid"]))
            self._answers[qid] = {"answer": a, "qid": qid}


    def save_answers(self, fname=RESPONSE_FILE):
        df = pd.DataFrame([a for a in self._answers.values()])
        df.to_csv(fname, index=False)



