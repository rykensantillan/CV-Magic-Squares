"""
Made by: Ryken Santillan
Version Started: 2022-12-27
Version Finished: 2023-01-01
Program: Magic Squares
Description:
      - This program reads a 3x3 magic square
        using pytesseract. After reading it,
        the data is sent to be processed
        and solved.
"""

from Solver import run
from Display import produceImg
from ImageReader import processImage

fileName = 'magic-squares-test-notViable.png'
produceImg((run((processImage(fileName)))))