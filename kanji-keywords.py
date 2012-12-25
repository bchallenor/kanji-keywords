# encoding: utf-8

# Kanji Keywords Anki plugin
#
# Adds keyword hints to kanji in your sentence/vocab decks
# Uses your own keywords from your kanji deck
#
# Copyright (C) 2012 Ben Challenor
# MIT license

from PyQt4.QtGui import *
from PyQt4.QtCore import *

from aqt import mw
from aqt.utils import showInfo

KANJI_MODEL_NAME = 'Kanji'
KANJI_FIELD_NAME = 'Kanji'
KEYWORD_FIELD_NAME = 'Keyword'

JAPANESE_MODEL_NAME = 'Japanese'
KEYWORD_HINTS_FIELD_NAME = 'Keyword-Hints'


def getMatchingModel(models, expectedModelName, expectedFieldNames):
  model = models.byName(expectedModelName)
  if not model:
    raise Exception('Cannot find model "%s".' % (expectedModelName))

  fieldNames = models.fieldNames(model)
  for expectedFieldName in expectedFieldNames:
    if not expectedFieldName in fieldNames:
      raise Exception('Cannot find field "%s" on model "%s".' % (expectedFieldName, expectedModelName))

  return model


def matchModel(models, model, expectedModelName, expectedFieldNames):
  if expectedModelName not in model['name']:
    return False

  fieldNames = models.fieldNames(model)
  for expectedFieldName in expectedFieldNames:
    if not expectedFieldName in fieldNames:
      return False

  return True


def getNidsForMatchingModel(models, expectedModelName, expectedFieldNames):
  for model in models.all():
    if matchModel(models, model, expectedModelName, expectedFieldNames):
      for nid in models.nids(model):
        yield nid


def getKanjiToKeyword(col):
  models = col.models

  kanjiModel = getMatchingModel(models, KANJI_MODEL_NAME, [KANJI_FIELD_NAME, KEYWORD_FIELD_NAME])
  kanjiModelId = kanjiModel['id']

  kanjiToKeyword = {}

  kanjiNoteIds = models.nids(kanjiModel)
  for kanjiNoteId in kanjiNoteIds:
    kanjiNote = col.getNote(kanjiNoteId)
    kanji = kanjiNote[KANJI_FIELD_NAME]
    keyword = kanjiNote[KEYWORD_FIELD_NAME]
    kanjiToKeyword[kanji] = keyword

  return kanjiToKeyword


def updateKeywordHints(col, kanjiToKeyword, nid):
  note = col.getNote(nid)

  note[KEYWORD_HINTS_FIELD_NAME] = 'hints'

  #note.flush()


def run(col):
  kanjiToKeyword = getKanjiToKeyword(col)

  #showInfo(str(kanjiToKeyword[u'家']))

  count = 0

  for nid in getNidsForMatchingModel(col.models, JAPANESE_MODEL_NAME, [KEYWORD_HINTS_FIELD_NAME]):
    updateKeywordHints(col, kanjiToKeyword, nid)
    count += 1

  showInfo('Updated %d notes' % (count))


a = QAction(mw)
a.setText('Kanji Keywords')
mw.form.menuTools.addAction(a)
mw.connect(a, SIGNAL('triggered()'), lambda: run(mw.col))

