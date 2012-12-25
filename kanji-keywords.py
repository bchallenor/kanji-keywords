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


def getModel(models, expectedModelName, expectedFieldNames):
  model = models.byName(expectedModelName)
  if not model:
    raise Exception('Cannot find model "%s".' % (expectedModelName))

  fieldNames = models.fieldNames(model)
  for expectedFieldName in expectedFieldNames:
    if not expectedFieldName in fieldNames:
      raise Exception('Cannot find field "%s" on model "%s".' % (expectedFieldName, expectedModelName))

  return model


def run(col):
  models = col.models

  kanjiModel = getModel(models, KANJI_MODEL_NAME, [KANJI_FIELD_NAME, KEYWORD_FIELD_NAME])

  kanjiModelId = kanjiModel['id']

  kanjiToKeyword = {}

  kanjiNoteIds = models.nids(kanjiModel)
  for kanjiNoteId in kanjiNoteIds:
    kanjiNote = col.getNote(kanjiNoteId)
    kanji = kanjiNote[KANJI_FIELD_NAME]
    keyword = kanjiNote[KEYWORD_FIELD_NAME]
    kanjiToKeyword[kanji] = keyword

  showInfo(str(kanjiToKeyword[u'家']))

a = QAction(mw)
a.setText('Kanji Keywords')
mw.form.menuTools.addAction(a)
mw.connect(a, SIGNAL('triggered()'), lambda: run(mw.col))

