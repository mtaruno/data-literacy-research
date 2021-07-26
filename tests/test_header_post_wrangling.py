import unittest
import sys
from pathlib import Path

if __package__ is None:                  
    DIR = Path(__file__).resolve().parent
    sys.path.insert(0, str(DIR.parent))
    __package__ = DIR.name

# from . import variable_in__init__py
# from . import other_module_in_package

from utilities.utils import preprocess_heading_text


class TestHeaderPostWrangling(unittest.TestCase):
    def test_preprocess_heading_text(self):
        text = "I would like to test ;; with a lot of PUNCTUATION and upper case and \
        stop words including and and and and if this will work!?!"

        print(preprocess_heading_text(text))
    
    def test_preprocess_heading_text_with_series(self):
        import pandas as pd
        series = pd.Series(['TESTING IF !!?? THIS WOULD WORK', 'SECOND test IF !??@#$'])
        series = series.apply(preprocess_heading_text)
        print(series)
        
unittest.main()