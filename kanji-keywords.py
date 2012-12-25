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

def assertContainsField(models, model, fieldName):
  modelFieldNames = models.fieldNames(model)
  if fieldName not in modelFieldNames:
    modelName = model['name']
    raise Exception('Model %s must contain field %s' % (modelName, fieldName))

def run(col):
  models = col.models

  kanjiModel = models.byName(KANJI_MODEL_NAME)
  kanjiModelId = kanjiModel['id']

  assertContainsField(models, kanjiModel, KANJI_FIELD_NAME)
  assertContainsField(models, kanjiModel, KEYWORD_FIELD_NAME)

  kanjiToKeyword = {}

  kanjiNoteIds = models.nids(kanjiModel)
  for kanjiNoteId in kanjiNoteIds:
    kanjiNote = col.getNote(kanjiNoteId)
    kanji = kanjiNote['Kanji']
    keyword = kanjiNote['Keyword']
    kanjiToKeyword[kanji] = keyword

  showInfo(str(kanjiToKeyword[u'家']))

a = QAction(mw)
a.setText('Kanji Keywords')
mw.form.menuTools.addAction(a)
mw.connect(a, SIGNAL('triggered()'), lambda: run(mw.col))

