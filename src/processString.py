from __future__ import annotations
#! ^^^^^ this is a future import, it moves the annotations evaluation to *after* the class definition

import json

from telegram import Update
from telegram.ext import CallbackContext

from state import State
from sym import Symbol

from anything import union, difference
from result import Result

from context import Context

