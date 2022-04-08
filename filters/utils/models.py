from dataclasses import dataclass
import logging
from typing import List
from panflute import stringify, Header, Div
import string


@dataclass
class Exercise:
  id: string
  title: string
  time: string
  elem: Header

  def __init__(self, id, title, time, elem) -> None:
    self.id = id
    self.title = title
    self.time = time
    self.elem = elem

  def get_from_elem(elem):
    logging.info("get_from_elem")
    logging.info(elem)
    return Exercise(
      id=elem.attributes["id"] if "id" in elem.attributes else "", 
      title=stringify(elem),
      time=elem.attributes["time"] if "time" in elem.attributes else "",
      elem=elem)

@dataclass
class Solution:
  exercise: Exercise
  elem: Div

  def __init__(self, exercise, elem) -> None:
    self.exercise = exercise
    self.elem = elem

@dataclass
class Expectation:
  content: string
  points: float
  bonuspoints: float

  def __init__(self, content, points, bonuspoints = 0) -> None:
      self.content = content
      self.points = points
      self.bonuspoints = bonuspoints


@dataclass
class ExerciseExpectation:
  exercise: Exercise
  expectations: List[Expectation]

  def __init__(self, exercise, expectations) -> None:
    self.exercise = exercise
    self.expectations = expectations
